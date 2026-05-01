#!/usr/bin/env python3
"""
LLM classification of untagged GitHub issues using our 14-category tag taxonomy.

Reads from issues_with_content.csv (produced by scrape_issue_content.py).
Targets only rows where tags == [] and fetch_status == ok.
Uses OpenRouter API with a configurable model.

Usage:
    python llm_classify_untagged.py
    MODEL_ID=qwen/qwen3.6-flash python llm_classify_untagged.py
    DRY_RUN=1 python llm_classify_untagged.py   # prints first 3 prompts, exits

Prerequisite:
    python scrape_issue_content.py   # builds issues_with_content.csv first
"""

import os, time, json, re
import pandas as pd
import requests
import backoff
from pathlib import Path
from dotenv import load_dotenv

# ── Config ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
ROOT_DIR = BASE_DIR.parent

load_dotenv(ROOT_DIR / ".env", override=True)

OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
MODEL_ID           = os.environ.get("MODEL_ID", "qwen/qwen3.6-flash")
MAX_RETRIES        = int(os.environ.get("MAX_RETRIES", "3"))
RETRY_DELAY        = float(os.environ.get("RETRY_DELAY", "2.0"))
MIN_YEAR           = int(os.environ.get("MIN_YEAR", "2018"))
DRY_RUN            = os.environ.get("DRY_RUN", "0") == "1"
CONTENT_FILE       = BASE_DIR / "issues_with_content.csv"
OUT_FILE           = BASE_DIR / f"llm_classified_issues_{MODEL_ID.replace('/', '_')}.csv"

# ── 14-category taxonomy (derived from categories.csv + tag-to-category mapping) ──
CATEGORIES = [
    "Bug Fixes and Defects",
    "Code Quality",
    "Community Engagement and Support",
    "Configuration",
    "Continuous Integration and Deployment (CI/CD)",
    "Documentation",
    "Feature Development and Enhancement",
    "Integration and Interfacing",
    "Libraries",
    "Licensing",
    "Code Components",
    "Release Management and Versioning",
    "User Interface and Outputs",
    "Technical Debt",
]

CATEGORY_DESCRIPTIONS = {
    "Bug Fixes and Defects":
        "Issues reporting incorrect behavior, crashes, false positives/negatives, regressions, or test failures.",
    "Code Quality":
        "Refactoring, validation improvements, performance, code style, linting, and non-functional code improvements.",
    "Community Engagement and Support":
        "Help-wanted requests, questions from users, community discussions, mentorship (GSoC/LFX), upstream coordination.",
    "Configuration":
        "Installation, packaging, Docker, Helm, dependency management, environment setup.",
    "Continuous Integration and Deployment (CI/CD)":
        "CI pipeline issues, GitHub Actions, CD workflows, automated build and test infrastructure.",
    "Documentation":
        "Missing, incorrect, or improved documentation, API docs, examples, READMEs.",
    "Feature Development and Enhancement":
        "New features, enhancements, proposals, must-have / nice-to-have improvements.",
    "Integration and Interfacing":
        "Support for specific ecosystems (Java, JS, Go, Python, OS), webhooks, plugin integrations, OS support.",
    "Libraries":
        "Core library / API issues, spdx-utils, internal library components.",
    "Licensing":
        "License detection, copyright scanning, license review, new license submissions, SPDX license list.",
    "Code Components":
        "Package scanning, serialization, data model, parsers, analyzers, scanners, I/O, package formats.",
    "Release Management and Versioning":
        "Breaking changes, release planning, versioning, changelogs, pending releases.",
    "User Interface and Outputs":
        "GUI, CLI output, end-user-facing behavior, report formats.",
    "Technical Debt":
        "Technical debt cleanup, refactoring debt, long-term maintenance work explicitly labeled as debt.",
}

CATEGORY_LIST_STR = "\n".join(f"  {i+1:2d}. {c}" for i, c in enumerate(CATEGORIES))

SYSTEM_PROMPT = f"""You are an expert software engineering researcher classifying GitHub issues from SBOM (Software Bill of Materials) tool repositories.

You will be given a GitHub issue title and body. Classify it into ONE OR MORE of the following 14 categories (most issues belong to 1-2 categories):

{CATEGORY_LIST_STR}

Category descriptions:
{chr(10).join(f'  - {c}: {d}' for c, d in CATEGORY_DESCRIPTIONS.items())}

Rules:
- Only assign categories you are HIGHLY CONFIDENT apply. If you are not certain, do not include the category.
- If no category fits with high confidence, return an empty list — do NOT force a category.
- Most issues warrant 1 category; a clearly multi-topic issue may warrant 2-3.
- Respond with ONLY a JSON object: {{"categories": ["<exact category name>", ...], "reasoning": "<one sentence>"}}
- Do not include a confidence field — all returned categories are implicitly high-confidence.
- Do not add any text outside the JSON object.
"""

# ── Load untagged issues from content cache ──────────────────────────────────

def load_untagged() -> pd.DataFrame:
    """
    Read issues_with_content.csv (from scrape_issue_content.py).
    Filters to: fetch_status==ok, year>=MIN_YEAR, tags empty.
    """
    if not CONTENT_FILE.exists():
        raise FileNotFoundError(
            f"{CONTENT_FILE} not found.\n"
            "Run scrape_issue_content.py first to build the content cache."
        )

    df = pd.read_csv(CONTENT_FILE)

    # Year filter
    df["created_at"] = pd.to_datetime(df["created_at"], utc=True, errors="coerce")
    df = df[df["created_at"].dt.year >= MIN_YEAR].copy()

    # Only successfully fetched rows
    df = df[df["fetch_status"] == "ok"].copy()

    # Empty-tag filter
    def is_untagged(val):
        if pd.isna(val):
            return True
        return str(val).strip() in ("[]", "", "nan")

    df = df[df["tags"].apply(is_untagged)].copy()

    spdx_n = (df["format"] == "spdx").sum()
    cdx_n  = (df["format"] == "cdx").sum()
    print(f"  Untagged (>=2018, fetch ok): spdx={spdx_n}  cdx={cdx_n}  total={len(df)}")
    return df


# ── OpenRouter API call ──────────────────────────────────────────────────────

class _RateLimited(Exception):
    pass


@backoff.on_exception(
    backoff.expo,
    (requests.exceptions.Timeout, requests.exceptions.ConnectionError, _RateLimited),
    max_tries=8,
    base=2,
    factor=1.5,
    jitter=backoff.full_jitter,
    on_backoff=lambda d: print(f"    backoff {d['wait']:.1f}s"),
)
def _call_api(payload: dict, headers: dict) -> str:
    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30,
    )
    if resp.status_code in (429, 503):
        raise _RateLimited(f"HTTP {resp.status_code}")
    resp.raise_for_status()
    data = resp.json()
    msg = (data.get("choices") or [{}])[0].get("message", {})
    content = msg.get("content")
    if not content:
        # Some reasoning models put answer only in reasoning text; extract from there
        reasoning = msg.get("reasoning", "") or ""
        for detail in msg.get("reasoning_details", []):
            reasoning += detail.get("text", "")
        if reasoning:
            return reasoning
        raise ValueError(f"empty content, finish_reason={((data.get('choices') or [{}])[0].get('finish_reason'))}")
    return content.strip()


def _valid_categories(cats) -> list[str]:
    """Return only category names that are in the taxonomy."""
    if isinstance(cats, str):
        cats = [cats]
    return [c for c in (cats or []) if c in CATEGORIES]


def classify_issue(title: str, body: str, url: str) -> dict:
    """Returns dict with 'categories' (list), 'confidence', 'reasoning'."""
    user_msg = f"GitHub issue URL: {url}\n\nTitle: {title}\n\nBody (truncated to 800 chars):\n{body[:800]}"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/wip-24-ali-sbom-emse",
        "X-Title": "SBOM Issue Classifier",
    }
    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_msg},
        ],
        "temperature": 0.0,
        "max_tokens": 1024,
    }

    for attempt in range(MAX_RETRIES):
        try:
            content = _call_api(payload, headers)
            if '{' in content:
                decoder = json.JSONDecoder()
                braces = list(re.finditer(r'\{', content))

                def _scan(positions):
                    for m in positions:
                        try:
                            obj, _ = decoder.raw_decode(content, m.start())
                            cats = obj.get("categories") or ([obj["category"]] if obj.get("category") else [])
                            if _valid_categories(cats):
                                return obj
                        except json.JSONDecodeError:
                            continue
                    return None

                # Forward pass (normal models put JSON first)
                found_result = _scan(braces)
                # Backward pass (reasoning models put JSON last)
                if found_result is None:
                    found_result = _scan(reversed(braces))

                if found_result is not None:
                    valid = _valid_categories(
                        found_result.get("categories") or
                        ([found_result["category"]] if found_result.get("category") else [])
                    )
                    return {
                        "categories": valid,
                        "confidence": "high",
                        "reasoning":  found_result.get("reasoning", ""),
                    }

                # Check if any JSON object has explicit empty categories (off-topic/spam)
                for m in braces:
                    try:
                        obj, _ = decoder.raw_decode(content, m.start())
                        if isinstance(obj.get("categories"), list) and obj["categories"] == []:
                            print(f"    SKIP: off-topic/spam: {obj.get('reasoning','')[:120]}")
                            return {"categories": [], "confidence": "high", "reasoning": obj.get("reasoning", "")}
                    except json.JSONDecodeError:
                        continue

                print(f"    WARNING: no category found in response ({len(content)} chars): {content[-300:]!r}")
        except Exception as e:
            short = str(e)[:120]
            print(f"    err attempt {attempt+1}: {short}")
        time.sleep(RETRY_DELAY * (attempt + 1))

    raise RuntimeError(f"All {MAX_RETRIES} retries exhausted for {url}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print(f"Model:    {MODEL_ID}")
    print(f"Output:   {OUT_FILE}")
    print(f"Source:   {CONTENT_FILE}")
    print(f"Min year: {MIN_YEAR}\n")

    all_untagged = load_untagged()

    if DRY_RUN:
        print("\n── DRY RUN: first 3 issues ──")
        for _, row in all_untagged.head(3).iterrows():
            print(f"\nURL:    {row['issue_url']}")
            print(f"Format: {row['format']}")
            print(f"Title:  {row['title']}")
            print(f"Body:   {str(row['body'])[:200]}\n---")
        return

    # Resume support (done_urls = unique issue URLs, since output is exploded)
    if OUT_FILE.exists():
        done = pd.read_csv(OUT_FILE)
        done_urls = set(done["issue_url"].dropna().unique().tolist())
        print(f"Resuming: {len(done_urls)} issues already classified ({len(done)} rows)")
    else:
        done = pd.DataFrame()
        done_urls = set()

    results = []
    remaining = [r for _, r in all_untagged.iterrows() if str(r["issue_url"]) not in done_urls]
    total_new = len(remaining)
    print(f"  Issues left to label: {total_new}")

    for new_i, row in enumerate(remaining, 1):
        url = str(row["issue_url"])
        fmt   = str(row["format"])
        repo  = str(row.get("repo", ""))
        title = str(row.get("title", ""))
        body  = str(row.get("body", ""))

        print(f"  [{new_i}/{total_new}] {fmt.upper()} | {title[:65]}")
        try:
            result = classify_issue(title, body, url)
        except RuntimeError as e:
            _save(done, results)
            print(f"\nFATAL: {e}\nProgress saved. Exiting.")
            return
        cats = result["categories"]
        if not cats:
            print(f"           → SKIPPED (off-topic/spam, no categories)")
            done_urls.add(url)  # don't revisit on resume
            continue
        print(f"           → {', '.join(cats)}")

        results.append({
            "issue_url":      url,
            "format":         fmt,
            "repo":           repo,
            "created_at":     row.get("created_at", ""),
            "title":          title,
            "llm_categories": str(cats),
            "model":          MODEL_ID,
        })

        if len(results) % 100 == 0:
            _save(done, results)
            print(f"  [checkpoint] {len(done) + len(results)} issues saved")

        time.sleep(0.3)

    _save(done, results)
    final = pd.concat([done, pd.DataFrame(results)], ignore_index=True) if results else done
    print(f"\nDone. {len(final)} issues classified → {OUT_FILE}")


def _save(done: pd.DataFrame, new_rows: list[dict]):
    rows = pd.DataFrame(new_rows)
    out  = pd.concat([done, rows], ignore_index=True) if not done.empty else rows
    out.to_csv(OUT_FILE, index=False)


if __name__ == "__main__":
    main()
