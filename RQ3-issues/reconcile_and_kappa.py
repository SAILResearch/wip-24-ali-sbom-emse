"""
Reconcile two LLM-annotated issue CSVs (minimax-m2.7 and qwen3.6-flash) and compute
inter-rater agreement metrics.

Both input CSVs contain only high-confidence tags (llm_confidence column removed).

Agreement metrics (on N_SAMPLE random issues):
  - Cohen's Kappa: per-category binary kappa + macro average
  - Krippendorff's Alpha: single overall alpha across all categories simultaneously
    (reliability matrix: 2 raters × (N_SAMPLE × 14) units, nominal level)

Reconciliation rule (intersection):
  - Accept category iff BOTH models assigned it
  - Single-model assignments are rejected (no corroboration)

Outputs:
  kappa_llm_reconcile.csv   -- per-category Cohen's Kappa + macro avg + Krippendorff's Alpha
  llm_issues_reconciled.csv -- final exploded tags (one row per issue x category, all issues)
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import cohen_kappa_score
import krippendorff

QWEN_FILE = Path("RQ3-issues/llm_classified_issues_qwen_qwen3.6-flash.csv")
MINI_FILE = Path("RQ3-issues/llm_classified_issues_minimax_minimax-m2.7.csv")
KAPPA_OUT = Path("RQ3-issues/kappa_llm_reconcile.csv")
RECONCILED_OUT = Path("RQ3-issues/llm_issues_reconciled.csv")

N_SAMPLE = int(os.environ.get("N_SAMPLE", 376))
SEED = int(os.environ.get("SEED", 42))

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


def binary_matrix(df: pd.DataFrame, issues: pd.Index) -> pd.DataFrame:
    """One row per issue, one column per category, value = 1 if assigned."""
    assigned = df[["issue_url", "llm_category"]].copy()
    assigned["val"] = 1
    wide = assigned.pivot_table(
        index="issue_url", columns="llm_category", values="val", aggfunc="max", fill_value=0
    )
    return wide.reindex(index=issues, columns=CATEGORIES, fill_value=0)


def main():
    print("Loading files...")
    df_q = pd.read_csv(QWEN_FILE)
    df_m = pd.read_csv(MINI_FILE)

    print(f"  qwen rows: {len(df_q)}, unique issues: {df_q['issue_url'].nunique()}")
    print(f"  minimax rows: {len(df_m)}, unique issues: {df_m['issue_url'].nunique()}")

    all_issues = pd.Index(
        sorted(set(df_q["issue_url"].unique()) | set(df_m["issue_url"].unique()))
    )
    print(f"  total unique issues (union): {len(all_issues)}")

    # ── Step 1: Sample issues for agreement computation ───────────────────────
    print(f"\nSampling {N_SAMPLE} issues (seed={SEED}) for agreement computation...")
    sampled_issues = pd.Index(
        pd.Series(all_issues).sample(n=min(N_SAMPLE, len(all_issues)), random_state=SEED).values
    )
    q_bin = binary_matrix(df_q, sampled_issues)
    m_bin = binary_matrix(df_m, sampled_issues)

    # ── Step 2: Cohen's Kappa per category ───────────────────────────────────
    print("Computing per-category Cohen's Kappa...")
    kappa_rows = []
    for cat in CATEGORIES:
        k = cohen_kappa_score(q_bin[cat], m_bin[cat])
        kappa_rows.append({"metric": "cohen_kappa", "category": cat, "value": round(k, 4)})

    macro_kappa = round(
        sum(r["value"] for r in kappa_rows) / len(kappa_rows), 4
    )
    kappa_rows.append({"metric": "cohen_kappa", "category": "MACRO_AVG", "value": macro_kappa})

    # ── Step 3: Krippendorff's Alpha (overall, all categories jointly) ────────
    # Reliability matrix shape: (n_raters=2) × (n_units = N_SAMPLE × 14)
    # Each (issue, category) cell is one unit; both models are the two raters.
    # level_of_measurement="nominal" is correct for binary 0/1 labels.
    print("Computing Krippendorff's Alpha (overall, nominal)...")
    reliability_matrix = np.array([
        q_bin.values.flatten().astype(float),
        m_bin.values.flatten().astype(float),
    ])
    alpha = round(krippendorff.alpha(
        reliability_data=reliability_matrix,
        level_of_measurement="nominal",
    ), 4)
    kappa_rows.append({"metric": "krippendorff_alpha", "category": "OVERALL", "value": alpha})

    # ── Print and save ────────────────────────────────────────────────────────
    out_df = pd.DataFrame(kappa_rows)
    out_df.to_csv(KAPPA_OUT, index=False)

    print(f"\nAgreement metrics (n={len(sampled_issues)} sampled issues, seed={SEED})")
    print(f"\n{'Metric':<22} {'Category':<50} {'Value':>8}")
    print("-" * 82)
    for row in kappa_rows:
        print(f"  {row['metric']:<20} {row['category']:<50} {row['value']:>8.4f}")

    # ── Step 4: Intersection reconciliation (all issues) ─────────────────────
    print(f"\nReconciling all {len(all_issues)} issues (intersection: both models must assign)...")
    q_all = binary_matrix(df_q, all_issues)
    m_all = binary_matrix(df_m, all_issues)

    final_binary = ((q_all == 1) & (m_all == 1)).astype(int)

    accepted_per_issue = final_binary.sum(axis=1)
    print(f"  Issues with ≥1 accepted category: {(accepted_per_issue > 0).sum()} / {len(all_issues)}")
    print(f"  Issues with 0 accepted categories: {(accepted_per_issue == 0).sum()}")
    print(f"  Total accepted (issue, category) pairs: {final_binary.values.sum()}")

    # ── Step 5: Explode to long format ───────────────────────────────────────
    long = (
        final_binary
        .rename_axis("issue_url")
        .reset_index()
        .melt(id_vars="issue_url", var_name="llm_category", value_name="accepted")
        .query("accepted == 1")
        .drop(columns="accepted")
    )

    meta_cols = ["issue_url", "format", "repo", "created_at", "title"]
    meta = (
        pd.concat([df_q[meta_cols], df_m[meta_cols]])
        .drop_duplicates(subset="issue_url")
        .set_index("issue_url")
    )
    long = long.join(meta, on="issue_url")
    long = long[["issue_url", "format", "repo", "created_at", "title", "llm_category"]]

    long.to_csv(RECONCILED_OUT, index=False)
    print(f"\nSaved {len(long)} rows to {RECONCILED_OUT}")
    print(f"Saved agreement metrics to {KAPPA_OUT}")


if __name__ == "__main__":
    main()
