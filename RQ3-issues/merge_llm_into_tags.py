"""
merge_llm_into_tags.py

Merges LLM-classified untagged issues into the existing tagged-issues files:
  cdx_issues_with_tags.csv  (augmented in-place)
  spdx_issues_with_tags.csv (augmented in-place)

For issues in sample_issues.csv, human_categories overrides qwen's llm_categories.

LLM rows are appended with Tags = category name (already in category-space).
categories.csv is extended with pass-through mappings so tags.R works unchanged.

Idempotent: re-running will not duplicate rows (checks by issue_url + Tags).
"""

import ast
import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent

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


def parse_cats(val) -> list[str]:
    if pd.isna(val) or str(val).strip() in ("", "[]"):
        return []
    try:
        result = ast.literal_eval(str(val))
        if isinstance(result, list):
            return [c for c in result if c in CATEGORIES]
    except Exception:
        pass
    return []


# ---------------------------------------------------------------------------
# 1. Load inputs
# ---------------------------------------------------------------------------
df_qwen   = pd.read_csv(BASE / "llm_classified_issues_qwen_qwen3.6-flash.csv")
df_sample = pd.read_csv(BASE / "sample_issues.csv")
df_cdx    = pd.read_csv(BASE / "cdx_issues_with_tags.csv")
df_spdx   = pd.read_csv(BASE / "spdx_issues_with_tags.csv")
df_cats   = pd.read_csv(BASE / "categories.csv")   # category, Tags, identifier

# Build human override map
human_override = {
    row["issue_url"]: parse_cats(row["human_categories"])
    for _, row in df_sample.iterrows()
    if parse_cats(row["human_categories"])
}

print(f"Qwen rows: {len(df_qwen)}, unique issues: {df_qwen['issue_url'].nunique()}")
print(f"Human overrides: {len(human_override)}")

# ---------------------------------------------------------------------------
# 2. Build exploded LLM rows in *_with_tags.csv schema
# ---------------------------------------------------------------------------
# Issue URL, State, Created At, Closed At, Tags, Repo, resolve_time_sec
llm_rows = []
for _, row in df_qwen.iterrows():
    url  = row["issue_url"]
    cats = human_override.get(url) or parse_cats(row["llm_categories"])
    for cat in cats:
        llm_rows.append({
            "Issue URL":        url,
            "State":            "open",
            "Created At":       row["created_at"],
            "Closed At":        "",
            "Tags":             cat,          # category name used directly as tag
            "Repo":             "https://github.com/" + row["repo"],
            "resolve_time_sec": 0.0,
            "_format":          row["format"],
        })

df_llm = pd.DataFrame(llm_rows)
print(f"LLM exploded rows: {len(df_llm)}")

# ---------------------------------------------------------------------------
# 3. Append to respective tagged-issues files (skip existing issue_url+Tags)
# ---------------------------------------------------------------------------
existing_cdx_keys  = set(zip(df_cdx["Issue URL"],  df_cdx["Tags"].astype(str)))
existing_spdx_keys = set(zip(df_spdx["Issue URL"], df_spdx["Tags"].astype(str)))

llm_cdx  = df_llm[df_llm["_format"] == "cdx"].drop(columns=["_format"])
llm_spdx = df_llm[df_llm["_format"] == "spdx"].drop(columns=["_format"])

new_cdx  = llm_cdx[~llm_cdx.apply(
    lambda r: (r["Issue URL"], r["Tags"]) in existing_cdx_keys, axis=1)]
new_spdx = llm_spdx[~llm_spdx.apply(
    lambda r: (r["Issue URL"], r["Tags"]) in existing_spdx_keys, axis=1)]

print(f"New CDX rows to append:  {len(new_cdx)}")
print(f"New SPDX rows to append: {len(new_spdx)}")

df_cdx_aug  = pd.concat([df_cdx,  new_cdx],  ignore_index=True)
df_spdx_aug = pd.concat([df_spdx, new_spdx], ignore_index=True)

df_cdx_aug.to_csv( BASE / "cdx_issues_with_tags.csv",  index=False)
df_spdx_aug.to_csv(BASE / "spdx_issues_with_tags.csv", index=False)

print(f"cdx_issues_with_tags.csv:  {len(df_cdx_aug)} rows")
print(f"spdx_issues_with_tags.csv: {len(df_spdx_aug)} rows")

# ---------------------------------------------------------------------------
# 4. Extend categories.csv with pass-through mappings (category → itself)
# ---------------------------------------------------------------------------
existing_passthrough = set(
    zip(df_cats["category"], df_cats["Tags"])
)

new_cat_rows = []
for cat in CATEGORIES:
    for identifier in ["CycloneDX", "SPDX"]:
        if (cat, cat) not in existing_passthrough:
            new_cat_rows.append({"category": cat, "Tags": cat, "identifier": identifier})

if new_cat_rows:
    df_cats_aug = pd.concat([df_cats, pd.DataFrame(new_cat_rows)], ignore_index=True)
    df_cats_aug.to_csv(BASE / "categories.csv", index=False)
    print(f"categories.csv extended with {len(new_cat_rows)} pass-through rows")
else:
    print("categories.csv already has pass-through rows — no change")
