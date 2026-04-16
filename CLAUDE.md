# SBOM Tool Ecosystem Study — CLAUDE.md

Empirical comparison of SPDX vs. CycloneDX tool ecosystems. Submitted to EMSE/TOSEM. Paper source in `wip-24-ali-sbom-emse/`, analysis code split across five folders below.

---

## Repository Layout

```
wip-24-ali-sbom-emse/     ← LaTeX paper source
  Main.tex
  Body/
    Methodology.tex       ← data collection & inter-rater agreement
    RQ1.tex               ← use-case analysis (NTIA taxonomy)
    RQ2.tex               ← OSS tool health (CHAOSS metrics)
    RQ3.tex               ← GitHub issue analysis
    RQ4.tex               ← CI-adopting project analysis
    Implications.tex
    RelatedWork.tex
    ThreatsToValidity.tex
  Figures/ Tables/

methodology-figure/       ← method.pptx/pdf (overview figure, logos)

RQ1-usecases/             ← RQ1: use-case classification
  sbom_tools.xlsx           main tool dataset (187 tools, open/prop, use cases)
  ntia_taxonomy_spdx_vs_cdx.R
  ntia_taxonomy_oss_vs_prop.R

RQ2-tools/                ← RQ2: tool ecosystem health
  CycloneNSpdxTools.csv     641 tool repos (SPDX + CycloneDX, incl. forks)
  main.ipynb                data collection + CHAOSS metric computation
  oss_tools_stats.r         statistical tests (Mann-Whitney, Cliff's Delta)
  bootstrapping.R           1,000-sample bootstrap CIs
  get_commit_contributor_mapping.py

RQ3-issues/               ← RQ3: GitHub issue analysis
  SpdxIssues.csv / CdxIssues.csv   raw issue reports
  spdx_issues_with_tags.csv / cdx_issues_with_tags.csv   tagged issues
  tags_sum.csv              49 CDX + 48 SPDX consolidated tags
  categories.csv / aggregatedCats.csv   14 issue categories
  issues_extraction.py / issues_extraction_chunks.py
  splitting_issues_in_tags.py
  issues.R / tags.R         statistical analysis + figures
  calctimediff.py           resolution-time computation

RQ4-project/              ← RQ4: CI-adopting project analysis
  top250_projects.csv       top-250 SPDX + top-250 CDX projects
  all_projects.csv          full 2,426-project dataset
  scrape.ipynb              GitHub search + CI snippet collection
  analysis.ipynb            project health metrics + language analysis
  projects_boxplots.r / ProjectStats_Boxplot.r
  top250_sampling.R / bootstrapping.R
  commit_count_quartile.csv / contributor_count_quartile.csv

comments/                 ← reviewer comments & rebuttals
  bram/1215/main.pdf        Bram's annotated PDF review (first round)
  bram/0415/rebuttal.docx   reviewer rebuttal text (original)
  bram/0415/rebuttal.md     extracted rebuttal with \bram{} inline comments
  bram/0415/rebuttal_response.docx   drafted rebuttal responses

requirements.txt          ← Python dependencies
```

---

## Key Numbers (quick reference)

| Item | Value |
|---|---|
| Tools manually analyzed (RQ1) | 187 (140 CDX sampled + 47 SPDX all) |
| Total tool repos (RQ2/RQ3) | 641 (171 CDX + 470 SPDX, incl. forks) |
| Issue reports analyzed (RQ3) | 33,840 (17,093 CDX + 16,747 SPDX, post-2018) |
| Tagged issues | 13,732 CDX (80.3%) + 11,746 SPDX (70.1%) |
| Issue categories | 14 |
| CI-adopting projects (RQ4) | 2,426 total → 1,394 single-format → top-250 each |
| SPDX tool-center date | collected at \collectdate |
| CycloneDX tool-center date | same |
| Inter-rater agreement metric | Krippendorff's Alpha (α = 0.72 initial, 0.85 final) |
| Age normalization | all metrics divided by repository age in days |
| 2018 cutoff rationale | CDX released May 2017; cutoff ensures comparable active period |

---

## Completed Analyses (from EMSE rebuttal — all done 2026-04-15)

1. **LDA topic modeling on issue tags** (R1.3 / R2.8) ✓
   - Applied LDA (k=14) to tag vocabulary of 25,433 tagged issues (post-2018)
   - Result: 14 topics closely mirror 14 hand-coded categories; no new themes beyond existing set
   - Untagged issues (8,407 = 24.8%) traced to spec/license repos → already in Licensing/Code Components
   - Added Section 4.3.4 to `Body/RQ3.tex`; filled [PENDING] in `rebuttal_response.docx` for R1.3 + R2.8

2. **SPDX 3.0 tool adoption check** (R1.4) ✓
   - Scanned all 456 SPDX repos (README, releases, changelogs) for SPDX 3.0 mentions (April 2026)
   - Result: 5 repos (1.1%) mention SPDX 3.0: tools-java, Spdx-Java-Library, tools-python, tools-golang, spdx-maven-plugin
   - All five are official SPDX core libraries; 98.9% not yet migrated
   - Added paragraph to `Body/ThreatsToValidity.tex` External Validity; filled [PENDING] in docx for R1.4
   - Raw results: `RQ2-tools/spdx3_adoption_results.csv`

3. **CI snippet use-case validation — extended to n=94** (R2.9 / R2.10) ✓
   - Stratified sample of 94 entries (36 SPDX + 58 CDX), satisfying Cochran criterion for ±10% margin at 95% CI over N=2,426
   - Of 87 fetchable: 81 Build-confirmed (93.1%; 95% CI: 85.8%–96.8%), 4 false positives (4.6%), 0 Consume/Transform
   - Dataset NOT pre-filtered: 71.5% of 3,458 tool_mention_links are non-CI files (Python, shell, Makefile, Gradle, JSON…)
   - Updated `Body/Methodology.tex` Section 3.4 and `Body/ThreatsToValidity.tex` Section 5.1
   - Updated R2.9 + R2.10 responses in `rebuttal_response.docx` with 3-level argument (conceptual + non-circular + stats)
   - Evidence: `RQ4-project/ci_validation_sample94.csv`

---

## Paper Fixes Applied (EMSE revision)

| Location | Change |
|---|---|
| `Methodology.tex` | Cohen's Kappa → Krippendorff's Alpha (both rounds) |
| `Methodology.tex` | Added NTIA taxonomy justification sentence with citations |
| `Methodology.tex` | Added fork inclusion rationale + fork-count covariate check |
| `Methodology.tex` | Added 2018 cutoff vs. age-normalization clarification |
| `Methodology.tex` | Added Build-use-case CI scope justification + 50-snippet validation |
| `RelatedWork.tex` | Added explicit comparison paragraph vs. Xia et al. (2023) |
| `Implications.tex` | Rewrote decision-making paragraph with 3 concrete scenario-based guidelines |
| `Implications.tex` | Rewrote issue implications with CDX bug-fix speed stat + SPDX 3.0 outlook |
| `ThreatsToValidity.tex` | Expanded tool-collection scope threat + GitHub fork complement |
| `ThreatsToValidity.tex` | Updated CI snippet validation to n=94, ±10% margin, 93.1% precision, 4.6% FP rate |
| `ThreatsToValidity.tex` | Added SPDX 3.0 adoption scan: 5/456 repos (1.1%) migrated as of April 2026 |
| `Methodology.tex` | Expanded CI validation paragraph: Cochran n=94, non-circular proof (71.5% non-CI files), Wilson CI |
| `RQ3.tex` | Added Section 4.3.4: LDA topic modeling validation of 14 issue categories |

---

## Running the Analysis

```bash
# Python environment
pip install -r requirements.txt

# RQ2 — tool health metrics
jupyter notebook RQ2-tools/main.ipynb

# RQ3 — issue collection
python RQ3-issues/issues_extraction.py
python RQ3-issues/splitting_issues_in_tags.py
Rscript RQ3-issues/issues.R
Rscript RQ3-issues/tags.R

# RQ4 — project collection + analysis
jupyter notebook RQ4-project/scrape.ipynb
jupyter notebook RQ4-project/analysis.ipynb
Rscript RQ4-project/projects_boxplots.r
```
