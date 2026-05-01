"""
Remove low- and medium-confidence rows from existing LLM classification CSVs.
Overwrites each file in-place, keeping only rows where llm_confidence == "high".

Usage:
    python RQ3-issues/filter_high_confidence.py
"""

from pathlib import Path
import pandas as pd

FILES = [
    Path("RQ3-issues/llm_classified_issues_minimax_minimax-m2.7.csv"),
    Path("RQ3-issues/llm_classified_issues_qwen_qwen3.6-flash.csv"),
]

for path in FILES:
    if not path.exists():
        print(f"SKIP (not found): {path}")
        continue

    df = pd.read_csv(path)
    before = len(df)
    issues_before = df["issue_url"].nunique()

    drop_cols = [c for c in ["llm_confidence", "llm_reasoning"] if c in df.columns]
    df_high = df[df["llm_confidence"] == "high"].drop(columns=drop_cols)
    after = len(df_high)
    issues_after = df_high["issue_url"].nunique()

    df_high.to_csv(path, index=False)
    print(
        f"{path.name}: {before} → {after} rows "
        f"({before - after} removed), "
        f"{issues_before} → {issues_after} unique issues"
    )
