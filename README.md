# The State of the SBOM Tool Ecosystems: A Comparative Analysis of SPDX and CycloneDX

[![arXiv](https://img.shields.io/badge/arXiv-2512.21781-b31b1b.svg)](https://arxiv.org/abs/2512.21781)
[![Project](https://img.shields.io/badge/Project-Website-2ea44f.svg)](https://sailresearch.github.io/26-ali-sbom-emse)

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
│   ├── ntia_taxonomy_oss_vs_prop.R     # NTIA taxonomy: OSS vs. proprietary tools
│   ├── ntia_taxonomy_spdx_vs_cdx.R    # NTIA taxonomy: SPDX vs. CycloneDX
│   └── sbom_tools.xlsx                # Tool dataset (sheets: SPDXAll, CycloneDXAll, final)
├── RQ2-tools/
│   ├── main.ipynb                     # Tool landscape analysis, Mann-Whitney U, Cliff's delta
│   ├── get_commit_contributor_mapping.py  # GitHub commit counts per contributor
│   ├── bootstrapping.R                # Bootstrap median with 95% CIs
│   ├── CycloneNSpdxTools.csv          # Tool repository statistics
│   ├── spdx3_adoption_results.csv     # SPDX 3 adoption results
│   └── *.pdf / *.pkl                  # Figures and serialized data
├── RQ3-issues/
│   ├── issues_extraction.py           # Extract GitHub issues (CycloneDX tools)
│   ├── issues_extraction_chunks.py    # Extract GitHub issues (SPDX tools, chunked)
│   ├── scrape_issue_content.py        # Scrape issue titles/bodies via GitHub API
│   ├── llm_classify_untagged.py       # LLM classification of issues into 14 categories
│   ├── merge_llm_into_tags.py         # Merge LLM labels with human tags
│   ├── splitting_issues_in_tags.py    # Split issues by tag into individual rows
│   ├── calculate_krippendorff_alpha.py  # Inter-rater reliability (Krippendorff's Alpha)
│   ├── calctimediff.py                # Issue resolution time calculation
│   ├── issues.R                       # Issue metrics, resolution time, trend analysis
│   ├── tags.R                         # Tag-based analysis
│   ├── CdxIssues.csv                  # Raw CycloneDX issues
│   ├── SpdxIssues.csv                 # Raw SPDX issues
│   ├── issues_with_content.csv        # Issues with scraped title/body and tags
│   ├── cdx_issues_with_tags.csv       # CycloneDX issues with human tags
│   ├── spdx_issues_with_tags.csv      # SPDX issues with human tags
│   ├── categories.csv                 # Final merged category labels
│   ├── sample_issues.csv              # Sampled issues for validation
│   └── *.pdf / *.xlsx                 # Figures and supplementary tables
├── RQ4-project/
│   ├── scrape.ipynb                   # GitHub metadata scraping (Selenium + GraphQL)
│   ├── analysis.ipynb                 # Project metrics, correlations, language distribution
│   ├── top250_sampling.R              # Stratified sampling with Wilcoxon validation
│   ├── bootstrapping.R                # Bootstrap mean with confidence intervals
│   ├── all_projects.csv               # Full project dataset
│   ├── top250_projects.csv            # Sampled top-250 projects
│   ├── top250_stats.csv               # Summary statistics for top-250 projects
│   ├── commit_count_quartile.csv      # Commit count quartile breakdown
│   ├── contributor_count_quartile.csv # Contributor count quartile breakdown
│   └── *.pdf                          # Figures
├── methodology-figure/
│   ├── method.pdf                     # Study methodology diagram (PDF)
│   ├── method.pptx                    # Study methodology diagram (editable)
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

## Citation

If you use this work, please cite our paper:

```bibtex
@misc{zhao2025statesbomtoolecosystems,
      title={The State of the SBOM Tool Ecosystems: A Comparative Analysis of SPDX and CycloneDX},
      author={Zhimin Zhao and Abdul Ali Bangash and Tongxu Ge and Arshdeep Singh and Zitao Wang and Bram Adams},
      year={2025},
      eprint={2512.21781},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={https://arxiv.org/abs/2512.21781},
}
```
