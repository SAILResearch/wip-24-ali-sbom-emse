# The State of the SBOM Tool Ecosystems: A Comparative Analysis of SPDX and CycloneDX

This repository contains the datasets, scripts, notebooks, and figures used in an empirical study of SBOM ecosystems, with a focus on SPDX and CycloneDX.

## Overview

The artifact is organized around four research-question-oriented modules:

- **RQ1-usecases**: use-case and taxonomy analysis for OSS vs. proprietary and SPDX vs. CycloneDX.
- **RQ2-tools**: SBOM tool landscape, metrics, and statistical analysis.
- **RQ3-issues**: issue mining, issue categorization, and issue-resolution analysis.
- **RQ4-project**: project-level analysis, sampling, validation, and correlations.

A separate folder, **methodology-figure**, provides visual materials for the study method.

## Repository Structure

```text
.
├── RQ1-usecases/
│   ├── ntia_taxonomy_oss_vs_prop.R
│   ├── ntia_taxonomy_spdx_vs_cdx.R
│   └── sbom_tools.xlsx
├── RQ2-tools/
│   ├── main.ipynb
│   ├── get_commit_contributor_mapping.py
│   ├── bootstrapping.R
│   ├── CycloneNSpdxTools.csv
│   ├── spdx3_adoption_results.csv
│   └── *.pdf / *.pkl
├── RQ3-issues/
│   ├── issues_extraction.py
│   ├── issues_extraction_chunks.py
│   ├── scrape_issue_content.py
│   ├── llm_classify_untagged.py
│   ├── merge_llm_into_tags.py
│   ├── splitting_issues_in_tags.py
│   ├── calculate_krippendorff_alpha.py
│   ├── calctimediff.py
│   ├── issues.R
│   ├── tags.R
│   └── *.csv / *.xlsx / *.pdf
├── RQ4-project/
│   ├── scrape.ipynb
│   ├── analysis.ipynb
│   ├── top250_sampling.R
│   ├── bootstrapping.R
│   └── *.csv / *.pdf
├── methodology-figure/
│   ├── method.pdf
│   ├── method.pptx
│   └── image assets
└── requirements.txt
```

## Data and Outputs

The repository includes both intermediate and final artifacts, including:

- Raw and processed CSV datasets.
- Analysis notebooks and scripts (Python/R).
- Statistical outputs and publication-ready figures (PDF).
- Supporting spreadsheets (XLSX) and serialized data (PKL).

## Environment

 This artifact uses both Python and R:
 - Python dependencies are listed in `requirements.txt`.
 - R is required for the analyses implemented in `.R` scripts, including those in `RQ1-usecases/`, `RQ2-tools/`, `RQ3-issues/`, and `RQ4-project/`.
 - Before reproducing the R-based analyses, install the R packages referenced by those scripts in your local R environment.

## Notes

- Reproduction commands are intentionally omitted for now.
- Some analyses are implemented in Python notebooks/scripts, while others are implemented in R scripts.
