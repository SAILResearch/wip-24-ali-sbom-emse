"""
Find a 368-issue sample whose Krippendorff's Alpha is close to a target value.

Strategy (deterministic, fast):
  1. Build binary matrices for all issues once.
  2. Compute a per-issue agreement score = number of categories where both models agree
     (both 1 or both 0). Higher score = more consistent pair.
  3. Sort all issues by agreement score descending.
  4. Start with the top-N_SAMPLE issues (highest agreement → highest alpha).
  5. Gradually swap the most-agreeing issue out for the next least-agreeing issue
     until alpha enters [TARGET - TOLERANCE, TARGET + TOLERANCE].

This is O(N) swaps and avoids random search entirely.

Usage:
    python RQ3-issues/find_sample_alpha.py
    TARGET=0.80 TOLERANCE=0.005 python RQ3-issues/find_sample_alpha.py
"""

import ast
import os
import numpy as np
import pandas as pd
from pathlib import Path
import krippendorff

QWEN_FILE  = Path("RQ3-issues/llm_classified_issues_qwen_qwen3.6-flash.csv")
MINI_FILE  = Path("RQ3-issues/llm_classified_issues_minimax_minimax-m2.7.csv")
SAMPLE_OUT = Path("RQ3-issues/sample_issues.csv")

N_SAMPLE  = int(os.environ.get("N_SAMPLE", 368))
TARGET    = float(os.environ.get("TARGET", 0.765))
TOLERANCE = float(os.environ.get("TOLERANCE", 0.005))

CATEGORIES = [
    "Bug Fixes and Defects",
    "Code Components",
    "Code Quality",
    "Community Engagement and Support",
    "Configuration",
    "Continuous Integration and Deployment (CI/CD)",
    "Documentation",
    "Feature Development and Enhancement",
    "Integration and Interfacing",
    "Libraries",
    "Licensing",
    "Release Management and Versioning",
    "Technical Debt",
    "User Interface and Outputs",
]


def build_binary_matrix(df: pd.DataFrame, issues: pd.Index) -> pd.DataFrame:
    exploded = (
        df[["issue_url", "llm_categories"]]
        .copy()
        .assign(llm_categories=lambda d: d["llm_categories"].apply(
            lambda v: ast.literal_eval(v) if isinstance(v, str) else []
        ))
        .explode("llm_categories")
        .rename(columns={"llm_categories": "llm_category"})
        .dropna(subset=["llm_category"])
    )
    exploded = exploded[exploded["llm_category"].isin(CATEGORIES)]
    exploded["val"] = 1
    wide = exploded.pivot_table(
        index="issue_url", columns="llm_category", values="val", aggfunc="max", fill_value=0
    )
    return wide.reindex(index=issues, columns=CATEGORIES, fill_value=0)


def compute_alpha(q_rows: np.ndarray, m_rows: np.ndarray) -> float:
    reliability_matrix = np.array([
        q_rows.flatten().astype(float),
        m_rows.flatten().astype(float),
    ])
    return krippendorff.alpha(
        reliability_data=reliability_matrix,
        level_of_measurement="nominal",
    )


def main():
    print("Loading files...")
    df_q = pd.read_csv(QWEN_FILE)
    df_m = pd.read_csv(MINI_FILE)
    print(f"  qwen:    {len(df_q)} issues")
    print(f"  minimax: {len(df_m)} issues")

    all_issues = pd.Index(
        sorted(set(df_q["issue_url"].unique()) | set(df_m["issue_url"].unique()))
    )
    print(f"  total unique issues (union): {len(all_issues)}")

    # ── Build full binary matrices once ──────────────────────────────────────
    print("Building binary matrices...")
    q_full = build_binary_matrix(df_q, all_issues).values  # shape (N, 14)
    m_full = build_binary_matrix(df_m, all_issues).values

    # ── Restrict pool to issues where BOTH models assigned ≥1 tag ────────────
    q_has_tag = q_full.sum(axis=1) > 0
    m_has_tag = m_full.sum(axis=1) > 0
    both_tagged = q_has_tag & m_has_tag
    pool_idx = np.where(both_tagged)[0]
    print(f"  issues where both models tagged: {len(pool_idx)} / {len(all_issues)}")

    if len(pool_idx) < N_SAMPLE:
        raise ValueError(f"Not enough doubly-tagged issues ({len(pool_idx)}) to fill sample of {N_SAMPLE}.")

    q_pool = q_full[pool_idx]
    m_pool = m_full[pool_idx]

    # ── Per-issue agreement score within the pool ─────────────────────────────
    agreement = (q_pool == m_pool).sum(axis=1)

    # Sort by agreement descending: most consistent first
    order = np.argsort(-agreement)
    print(f"  agreement scores: min={agreement.min()}, max={agreement.max()}, mean={agreement.mean():.2f}")

    # ── Start with top N_SAMPLE (highest agreement) ───────────────────────────
    selected = list(order[:N_SAMPLE])       # indices into pool_idx
    candidates = list(order[N_SAMPLE:])     # remaining pool indices, agreement desc

    alpha = compute_alpha(q_pool[selected], m_pool[selected])
    print(f"\nInitial alpha (top-{N_SAMPLE} most consistent): {alpha:.4f}")
    print(f"Target: {TARGET} ± {TOLERANCE}")

    if alpha < TARGET - TOLERANCE:
        print("Initial alpha already below target — try lowering TARGET or widening TOLERANCE.")
        return

    # ── Swap most-agreeing issue out, least-agreeing candidate in ─────────────
    step = 0

    while alpha > TARGET + TOLERANCE and candidates:
        out_idx = selected.pop(0)
        in_idx  = candidates.pop()   # least agreeing available candidate
        selected.append(in_idx)

        alpha = compute_alpha(q_pool[selected], m_pool[selected])
        step += 1

        if step % 50 == 0 or abs(alpha - TARGET) < TOLERANCE * 3:
            print(f"  step={step:4d}  alpha={alpha:.4f}  swapped agreement {agreement[out_idx]} → {agreement[in_idx]}")

        if alpha < TARGET - TOLERANCE:
            # Overshot — undo last swap, refine with single swaps
            selected.pop()
            selected.insert(0, out_idx)
            candidates.append(in_idx)
            print(f"  Overshot at step {step} (alpha={alpha:.4f}). Refining...")

            found = False
            for cand in reversed(candidates):
                for si in range(len(selected)):
                    trial = selected[:]
                    trial[si] = cand
                    a = compute_alpha(q_pool[trial], m_pool[trial])
                    if TARGET - TOLERANCE <= a <= TARGET + TOLERANCE:
                        selected = trial
                        alpha = a
                        found = True
                        print(f"  Refined: step={step}  alpha={alpha:.4f}")
                        break
                if found:
                    break
            break

    if TARGET - TOLERANCE <= alpha <= TARGET + TOLERANCE:
        print(f"\nFound sample with alpha={alpha:.4f} (target={TARGET} ± {TOLERANCE})")
    else:
        print(f"\nBest achieved alpha={alpha:.4f} (target={TARGET} ± {TOLERANCE}) — saving anyway.")

    # ── Save winning sample ───────────────────────────────────────────────────
    winning_urls = all_issues[pool_idx[selected]]

    meta_cols = ["issue_url", "format", "repo", "created_at", "title"]
    meta = (
        pd.concat([df_q[meta_cols], df_m[meta_cols]])
        .drop_duplicates(subset="issue_url")
        .set_index("issue_url")
    )

    cats_q = df_q.drop_duplicates(subset="issue_url").set_index("issue_url")["llm_categories"]
    cats_m = df_m.drop_duplicates(subset="issue_url").set_index("issue_url")["llm_categories"]

    out = (
        pd.DataFrame({"issue_url": winning_urls})
        .join(meta, on="issue_url")
        .join(cats_q.rename("qwen_categories"), on="issue_url")
        .join(cats_m.rename("minimax_categories"), on="issue_url")
    )
    out = out[["issue_url", "format", "repo", "created_at", "title", "qwen_categories", "minimax_categories"]]
    out.to_csv(SAMPLE_OUT, index=False)
    print(f"Saved {len(out)} issues to {SAMPLE_OUT}  (alpha={alpha:.4f})")


if __name__ == "__main__":
    main()
