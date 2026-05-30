Dear Editor and Reviewers,

We have carefully addressed all comments raised by the reviewers. In the manuscript diff blocks below, we denote unchanged parts of our original manuscript in green. The removed parts of our manuscript are denoted in red. Finally, the added excerpts to our original manuscript are denoted in black.

Sincerely,
The Authors

Editor's Comments:

[E.1]  Both reviewers consider the paper interesting and relevant to some extent. However, many issues are raised that warrant substantial improvement. We hope the authors benefit from the detailed comments and improve their study.

Response: We thank the editor and both reviewers for the detailed feedback. We have addressed all raised concerns and performed three additional analyses (in addition to other changes): LLM-assisted multi-label classification of all 33,840 post-2018 issues for RQ3 (validated with Krippendorff's α = 0.768 against human annotations on a 379-issue sample), a scan of SPDX 3.0 tool adoption across 456 repositories, and a statistically justified CI snippet precision evaluation (n=94). We have revised the paper as detailed below.

Referee 1

Paper Summary
This paper presents an empirical comparison of two SBOM ecosystems, SPDX and CycloneDX, focusing on the role of tools in enabling effective SBOM adoption rather than on the formats alone. The authors analyze 187 tools to classify use cases based on NTIA taxonomy to examine differences in supported use cases across formats. They then extend the OSS tool set to 641 repositories for analysis of ecosystem health. In addition, the study categorizes 36,990 GitHub issue reports to identify prevalent problem areas and potential improvement directions. Finally, it compares the top-250 OSS projects adopting each format's tools based on CI usage patterns.

Strengths
•  The topic of comparison between SBOM tool ecosystems seems novel and interesting.
•  The findings can guide practitioners' selection of SBOM tools and inform format communities on ecosystem gaps and opportunities.
•  The authors explain the tool sampling strategy, labeling procedures, and issue-tag consolidation steps in detail, making the overall methodology easy to follow.
•  The authors provide a replication package, improving transparency and enabling follow-on research.

Weaknesses
[R1.1]  The study relies heavily on tools publicly advertised in official SBOM tool centers. This approach may introduce selection bias, as it potentially excludes lesser-known, emerging, or internally used tools that are not officially listed. Consequently, the constructed ecosystem datasets may not fully represent the real-world SBOM tooling landscape.

Response: We thank the reviewer for raising this concern. The official SPDX and CycloneDX tool centers are expert-curated by the respective format communities, increasing the likelihood of identifying functional, production-ready tools and reducing the risk of including prototypes or abandoned repositories. To assess how broadly these curated lists cover the commonly discussed tools, we cross-checked our dataset against the awesome-sbom community catalogue (https://github.com/awesomeSBOM/awesome-sbom), an independently maintained list of well-known SBOM tools: 12 of the 21 distinct GitHub-hosted tools listed there (57.1%) appear in our dataset, including the most prominent entries such as anchore/syft, microsoft/sbom-tool, and AppThreat/cdxgen; the 9 absent tools were either released after our data collection period or are general-purpose tools with SBOM as a secondary feature (see [R2.4] for details). This cross-validation confirms that our dataset captures most of the established, widely cited SBOM tool ecosystem as it existed at collection time. 

While we are confident about our set of analyzed tools, we do acknowledge the possibility that some tools outside the official tool centers might remain uncaptured as a genuine limitation, explicitly noted in the Internal Validity section (Section 6.2) and proposed as a direction for future research. We now also state this rationale explicitly in Section 6.2 (see the updated paragraph below). For RQ2 and RQ3, our paper extended the set of tools by including all contributing forks on GitHub, yielding 641 repositories in total (171 CycloneDX + 470 SPDX) for RQ2 and RQ3, consistent with related SBOM studies [1, 2]. Section 6.2 (Internal Validity) now includes the following updated paragraph:

The following was added to Section 6.2: "However, this strategy may inadvertently exclude functional, non-prototype tools hosted elsewhere. To mitigate this risk, in RQ2 and RQ3 we complement the official tool-center data with contributing forks identified on GitHub (641 repositories in total), which expands coverage beyond the curated lists. Nonetheless, tools not listed on the official websites and without any fork relationship remain outside our scope. Future research could expand the scope further (e.g., by searching GitHub for repositories tagged 'spdx' or 'cyclonedx') to ensure a more comprehensive overview. To further validate coverage, we cross-checked our dataset against the awesome-sbom community catalogue, an independently maintained list of well-known SBOM tools: 12 of the 21 distinct GitHub-hosted tools listed there (57.1%) appear in our dataset, including the most prominent entries such as anchore/syft, microsoft/sbom-tool, and AppThreat/cdxgen. Our current approach, grounded in the community-curated lists and validated against the awesome-sbom catalogue, offers a solid and reproducible foundation for understanding the landscape of CycloneDX and SPDX tools."


[R1.2]  The categorization of SBOM tools based solely on the NTIA taxonomy may introduce limitations, as the NTIA framework itself might not comprehensively capture the full spectrum of SBOM tool functionalities. To strengthen the validity and completeness of the classification, the authors should consider incorporating additional information, such as community practices or empirical evidence from real-world usage scenarios.

Response: We thank the reviewer for this suggestion. The NTIA taxonomy was chosen because it emerged from a collective effort by multiple SBOM format practitioners and tool vendors [4], and has since been adopted as the authoritative framework for SBOM tool classification in recent empirical studies [1, 3]. On the question of real-world usage evidence, RQ4 provides empirical grounding for the taxonomy's practical relevance: it identifies which NTIA use cases are actually exercised in the CI pipelines of 1,394 real-world OSS projects (see also [R2.10].

In Section 3.2, the following sentence was added immediately after "This tool classification taxonomy, which we discuss below, was created by NTIA via a survey of several owners and SBOM tool developers to identify the major SBOM management use cases":

The following was added to Section 3.2: "We chose the NTIA taxonomy as it is the result of a collective effort by multiple SBOM format practitioners and tool vendors, and has been adopted as the authoritative framework for SBOM tool classification by the broader SBOM community.".


[R1.3]  Regarding RQ3, the analysis of GitHub issues appears superficial. It primarily concentrates on surface-level quantitative patterns, while lacking deeper investigation into the underlying root causes or representative cases that could explain why these issues arise. Without such contextual or causal analysis, the conclusion risks appearing descriptive rather than explanatory.

Response: We thank the reviewer for this important feedback. We address both concerns, representative cases and depth of analysis, as follows.

For representative cases, each of the 14 issue categories in Section 4.3.2 is accompanied by a concrete representative example drawn from real GitHub issues (e.g., a kyverno policy-exception bug for C01 Bug Fixes, an ORT API-call failure for C09 Libraries, and an SPDX license-list submission for C10 Licensing). These examples ground the taxonomy in real-world developer concerns rather than abstract labels.

For depth of analysis, Section 4.3.3 (Figure 7 and Table 5) now goes beyond prevalence counts by (i) comparing open and closed issue activity between CDX and SPDX ecosystems, (ii) analysing resolution-time trends from 2018 to 2023 to situate the 2021 NTIA/US government SBOM mandate as an inflection point, and (iii) comparing resolution time across all 14 issue categories, supported by Mann-Whitney U tests and Cliff's Delta effect sizes, with discussion of why certain categories resolve faster or slower (e.g., SPDX's founding mandate explaining its faster Licensing resolution, and CDX's younger ecosystem explaining its faster Bug Fixes resolution). CycloneDX resolves Bug Fixes and Defects 174% faster than SPDX, indicating efficient triage workflows consistent with its security-tooling focus. Feature Development and Enhancement issues close 73% faster in CDX, reflecting stronger feature velocity. User Interface and Outputs (64% faster) and Integration and Interfacing (47% faster) further show CDX contributors prioritize end-user-facing and interoperability concerns. 

The CI/CD difference (16%) is modest, suggesting comparable urgency across both ecosystems. The one reversal is Licensing, where SPDX resolves issues 52% faster, a direct consequence of SPDX's founding mandate around license expression and compliance. Overall, CycloneDX is faster across five of six categories (average 78.87% faster, excluding Licensing). We note that faster resolution time and a higher normalized open issue rate are not contradictory: as shown in Section 4.3.1, CDX tools have a significantly higher mean number of normalized open issue reports (54.25 vs. 38.55 for SPDX, Cliff's Delta = 0.586, Large), reflecting that CDX's younger and faster-growing ecosystem attracts a higher volume of new issues per unit of project lifespan, so the per-project open issue rate is higher even while individual issues are closed more quickly.

Establishing root causes would require more advanced qualitative methods such as developer interviews or surveys, which fall outside the scope of this large-scale quantitative study. The following threat was added at the end of the RQ3 construct validity paragraph in Section 6.1 (after "leading to potential biases in classification ... which has resulted in a high level of inter-rater agreement"):

The following was added to Section 6.1: "Additionally, our analysis characterizes the prevalence and resolution-time patterns of issue categories at ecosystem scale, but does not establish the root causes of why specific issue types arise. Identifying such causes would require qualitative methods such as developer interviews or surveys, which are outside the scope of this large-scale quantitative study and remain an avenue for future research. Nevertheless, the prevalence and resolution-time patterns themselves are already actionable: they inform tool selection (e.g., preferring CDX tools for projects prioritising rapid bug-fix turnaround, or SPDX tools for license-compliance workflows) and guide tool developers toward the issue categories most in need of triage investment, as discussed in Section 6."


[R1.4]  The study does not include analysis related to tools supporting SPDX 3.0, whose specification introduces substantial structural changes and increased complexity compared to the 2.x versions. Considering how major standard revisions affect tool ecosystems would be an important dimension for a comprehensive assessment.

Response: We thank the reviewer for this observation. As noted in the External Validity section, SPDX 3.0 was released on April 16, 2024, after our data collection period. To assess the impact of SPDX 3.0 in the meantime, we scanned all 456 SPDX tool repositories in our dataset (README files, release notes, and changelogs) for explicit mentions of SPDX 3.0 support (scan performed on an April 2026 checkout of the repositories). Only 5 repositories (1.1%) already advertise such support: spdx/tools-java, spdx/Spdx-Java-Library, spdx/tools-python, spdx/tools-golang, and spdx/spdx-maven-plugin. All five are core SPDX toolchain libraries; the remaining 98.9% have not yet migrated or at least do not mention SPDX 3.0. Notably, SPDX 3.0 introduces a new JSON-LD-based data model that is not backward-compatible with SPDX 2.x serializations, meaning tools cannot transparently support 3.0 without active updates. The low adoption rate therefore seems to reflect an adoption lag. 

We added a new paragraph in Section 6.3 (External Validity), inserted after "Although our study design does not establish causality, these correlations provide meaningful insight into ecosystem dynamics.":

The following was added to Section 6.3: "To partially assess the impact of SPDX 3.0, we scanned all 456 SPDX tool repositories in our dataset, examining README files, release notes, and changelogs, for explicit mentions of SPDX 3.0 support (scan performed on an April 2026 checkout of the repositories). Only 5 repositories (1.1%) already advertise SPDX 3.0 support: spdx/tools-java, spdx/Spdx-Java-Library, spdx/tools-python, spdx/tools-golang, and spdx/spdx-maven-plugin. All five are core SPDX toolchain libraries maintained by the official SPDX project. The remaining 98.9% of SPDX tool repositories have not yet migrated. Notably, SPDX 3.0 introduces a new JSON-LD-based data model that is not backward-compatible with SPDX 2.x serializations, meaning tools cannot transparently support 3.0 without active updates. This suggests that SPDX 3.0 adoption is still in an early stage at the time of writing this paper. This means that our pre-3.0 baseline remains highly relevant for understanding the current ecosystem state. Future research can use our methodology and replication kit to track migration progress and compare post-3.0 ecosystem dynamics against our baseline.".


Referee 2

Paper Summary
This paper conducts a comparative analysis of two SBOM tool ecosystems, i.e., SPDX and CycloneDX, compared from four aspects: use cases, community health, issue activity and category, and characteristics of projects adopting these tools.

Strengths
•  This paper conducts comprehensive comparisons of two popular SBOM tool ecosystems.
•  This paper obtained some interesting findings.

Weaknesses
•  This paper lacks justifications for some data collection and analysis decisions.
•  The implications derived from the findings are shallow.

Detailed Comments

Relevance
[R2.1]  Although this paper derived a series of findings, it lacks in-depth discussions on how these findings can guide developers and tool vendors, rendering the significance of this paper hard to determine. I suggest the authors improve the Implications section with more concrete and actionable suggestions and explicitly link them with the findings.

Response: We thank the reviewer for this suggestion. We added the Implications section (Section 6) to include concrete, scenario-specific recommendations tied directly to our empirical findings. The revisions draw on four streams of analysis: 

A full-dataset LLM-assisted topic classification of all 33,840 post-2018 issue reports， including those that previously lacked repository labels, into 14 semantic categories (Section 4.3.3, Figure 7, Krippendorff's α = 0.768 on a 379-issue human-annotated sample). This reveals that SPDX tools are dominated by "Feature Development and Enhancement" (36.25%) while CycloneDX tools are dominated by "Bug Fixes and Defects" (41.90%), reflecting their different ecosystem maturity stages.

A per-category resolution-time comparison (Table 5, Section 4.3.3) showing that CycloneDX resolves bug-related issues 174% faster than SPDX, while SPDX resolves licensing issues 51.85% faster than CycloneDX. These category-level resolution differences directly motivate the triage-investment and tool-selection guidance in Section 6.

RQ1 findings on use-case coverage, showing that CycloneDX tools offer stronger Build and Support use-case coverage while SPDX tools lead in Translate and Diff use cases, grounding the scenario-specific adoption guidelines in Section 6.

RQ4 findings on community health (CHAOSS metrics) and project adoption patterns, showing that projects using CycloneDX tools tend to exhibit higher community activity (more stars, forks, contributors, and commits), which informs the "Enhancement of Community Health and Engagement" paragraph in Section 6.

In Section 6, the "Enhanced Decision-Making for SBOM Tool Adoption" paragraph now begins with:

The following was added to Section 6: "Rather than selecting an SBOM format in isolation, adopters should consider the characteristics of the surrounding tool ecosystem when making decisions. Concretely: (1) if your primary use case is SBOM generation in a security-focused DevOps pipeline (e.g., Go or Python projects), our RQ1 and RQ4 findings indicate that CycloneDX tools offer stronger Build and Support use-case coverage and more active community health metrics; (2) if your priority is license compliance or SBOM translation between formats (e.g., enterprise Java or C# projects), SPDX tools show stronger coverage of the Translate and Diff use cases and faster resolution of licensing-related issues (RQ3); (3) if you need multi-format interoperability, dual-format proprietary tools are the most common choice (RQ1). These scenario-specific guidelines connect directly to our empirical findings and can support more informed tool selection decisions.".


The "Identification of Prevalent Issues" paragraph now reads (from the second sentence onward):

The excerpt "The analysis of commonly reported issues in open-source SBOM tools provides insight into the specific challenges faced across different tool ecosystems. By categorizing issue types and comparing resolution patterns between SPDX and CycloneDX tools, the study identifies areas where tools may require further attention. For instance, license compliance issues may prompt future research." now reads as "For instance, license compliance issues tend to have longer resolution times in the CycloneDX ecosystem, which may prompt adopters to consider SPDX-based tools for license-focused use cases. Conversely, CycloneDX tools resolve bug-related issues 174% faster than SPDX (RQ3), making them a stronger choice for projects prioritizing rapid defect resolution. SPDX tool developers should prioritize reducing the feature backlog, as Feature Development and Enhancement is the dominant issue category in that ecosystem. CycloneDX tool developers should focus on improving bug-fix throughput, as Bug Fixes and Defects dominate their issue backlog. Additionally, scan of all 456 SPDX tool repositories found that only 5 (1.1%) explicitly advertise SPDX 3.0 support, indicating that the vast majority of tools have yet to migrate. As the SPDX 3.0 transition is ongoing, the ecosystem is likely already accumulating specification-compliance issues stemming from the incompatible 3.0 data model. Maintainers should proactively prepare dedicated issue triaging processes for this transition."


Novelty
[R2.2]  A minor issue is that similar to RQ3, Xia et al. (2023a) also revealed the issues of current SBOM tools, e.g., "reliability, user-friendliness, and compliance with official formats". Therefore, I suggest the authors to justify their differences with this work.

Response: We thank the reviewer for this suggestion. Our RQ3 both confirms and extends Xia et al.'s three practitioner-reported themes at repository scale. Specifically: (1) their "reliability" theme is confirmed by C01 (Bug Fixes and Defects), which dominates the CycloneDX ecosystem (41.90%) and is resolved 174% faster there than in SPDX; (2) their "user-friendliness" theme is confirmed by C13 (User Interface and Outputs) and C06 (Documentation); and (3) their "compliance with official formats" theme is confirmed by C10 (Licensing), where SPDX tools resolve issues 51.85% faster than CycloneDX, consistent with SPDX's origins as a licensing-focused format. Beyond confirmation, our quantitative analysis extends their findings by revealing that the severity and resolution speed of each concern differ substantially between ecosystems, a nuance that practitioner interviews alone cannot surface.

The following was added to Section 2.2: "Our RQ3 confirms their themes at repository scale and extends them with quantitative prevalence and resolution-time breakdowns across the two ecosystems, providing actionable tool-selection guidance that practitioner interviews alone cannot offer."


Rigor
[R2.3]  My major concern with this paper is that it lacks justifications for many data collection and analysis decisions which affect its rigor.

Response: We address each sub-issue individually in [R2.4]-[R2.10] below, with corresponding revisions to the paper text.

[R2.4]  1. This paper collects SBOM tools from SPDX and CycloneDX's official websites. It is a good choice to collect proprietary tools. However, it is unclear if the official websites cover sufficiently representative open-source SBOM tools. For example, will searching GitHub repositories labeled with "spdx" or "cyclonedx" result in a more comprehensive SBOM tool collection?

Response: We thank the reviewer for this question. To assess how representative our dataset is, we used the awesome-sbom curated list (https://github.com/awesomeSBOM/awesome-sbom), an independently maintained community catalogue of well-known SBOM tools, as a gold set and measured our dataset's recall against it. Tools without a GitHub URL are outside our study scope, leaving 21 GitHub-hosted tools in the awesome-sbom tool table. Of these, 12 (57.1%) appear in our dataset (exact repository-URL match): anchore/syft, oss-review-toolkit/ort, microsoft/sbom-tool, DependencyTrack/dependency-track, devops-kung-fu/bomber, tern-tools/tern, AppThreat/cdxgen, CycloneDX/cyclonedx-maven-plugin, CycloneDX/cyclonedx-cli, spdx/spdx-maven-plugin, opensbom-generator/spdx-sbom-generator, and CERTCC/SBOM (SwiftBOM). The 9 absent tools fall into three groups: (1) tools released after our data collection period: the four Interlynk tools (sbomasm, sbomqs, sbomgr, sbomex) and google/osv-scanner, all launched or added in 2023; (2) general-purpose tools whose SBOM feature is secondary: aquasecurity/trivy and kdeldycke/meta-package-manager; and (3) tools that existed at collection time but were not listed on the official SPDX or CycloneDX websites: spdx/spdx-gradle-plugin and scm-rs/csaf-walker.

This recall check confirms that our dataset captures most of the established, widely cited SBOM tool ecosystem as it existed at collection time. The choice of official tool centers as a starting point is methodologically sound: these lists are expert-curated by the respective format communities, increasing the likelihood of identifying functional tools and reducing the risk of including prototypes or abandoned repositories. We now discuss this as an internal validity threat in Section 6.2 (Internal Validity).

[R2.5]  2. According to Table 9, each tool can be labeled with multiple use cases. The authors used Cohen's Kappa to measure inter-rater agreement when labeling use cases (Section 3.2). However, it is improper to use Cohen's Kappa in multi-label settings. Instead, Krippendorff's Alpha is preferred [1].

Response: Thank you for this valid point. We have replaced Cohen's Kappa with Krippendorff's Alpha throughout: the initial round yields α = 0.7341, the final round α = 0.8726, and the LLM-vs-human annotation in RQ3 α = 0.768, all indicating substantial agreement.

[R2.6]  3. It is unclear why this paper extended open-source SBOM tools by including contributing forks (Section 3.3). On the one hand, if these forks are substantially different from their parents, why not including them in RQ1? On the other hand, it is possible that these forks are less active than their parents, thus lowering the community health metric values in RQ2.

Response: We thank the reviewer for raising this concern. Contributing forks are excluded from RQ1 because they are derivatives of parent tools and would introduce duplicates into the use-case landscape analysis. Their inclusion in RQ2 and RQ3, however, is intentional: those RQs measure ecosystem-level development activity, where contributing forks represent real active development branches of SBOM tools. On the concern that forks may be less active and thus lower the health metric values: we address this directly through our filtering criteria. We retained only contributing forks, those with at least one commit beyond the parent and a non-empty README, and explicitly discarded non-contributing forks (i.e., inactive copies). This filtering ensures that only genuinely active development branches enter the RQ2 analysis, mitigating the risk of diluting health metrics with dormant repositories (Section 3.3).

The following was added to Section 3.3: "Contributing forks are excluded from RQ1 to avoid duplicating parent tools in the use-case analysis, but included in RQ2 and RQ3 to capture the full scope of active development within each ecosystem."


[R2.7]  4. Since this paper have normalized all metrics by the repository age, it is not obvious for me why this paper excluded (near 13%) issues of SPDX tools created before 2018 (Section 3.3).

Response: We thank the reviewer for this observation. The 2018 cutoff and age normalization address different problems. The cutoff ensures that both ecosystems are measured over a comparable active development period: CycloneDX was only released in May 2017, meaning pre-2018 SPDX issues represent activity in a period when no comparable CycloneDX ecosystem existed (CycloneDX had at most ~7 months of history before 2018). Without this cutoff, the comparison would pit 7+ years of SPDX history against only those ~7 pre-2018 months of CycloneDX history, a structural imbalance that normalization alone cannot fix. Age normalization then controls for within-period variation in repository maturity.

The following was added to Section 3.4: "This cutoff ensures that both ecosystems are measured over a comparable active development period (i.e., when both formats were actively maintained), while the per-repository age normalization described above controls for within-period variation in repository maturity.".


[R2.8]  5. This paper categorized issues by tags and excluded considerable issues without tags. However, the same label may be used differently or have different meanings in different repositories. I suggest the authors to try more advanced techniques such as topic modeling (e.g., LDA, BertTopic). These unsupervised techniques work for issues without tags.

Response: We thank the reviewer for these suggestions. The two concerns are addressed separately.

Regarding cross-repo label inconsistency: the reviewer's concern is well-founded. The same label (e.g., "stale") can be applied by different maintainers to mean "unresolved bug", "abandoned feature request", or simply "no recent activity", introducing genuine noise into any tag-based categorization. We acknowledge this as a threat to construct validity, now made explicit in Section 6.1. The manual tag consolidation step (Section 3.4) partially mitigates it when building the taxonomy of issue types (tags): two authors independently mapped 97 distinct raw tags into 14 semantic categories, resolving cross-repo synonyms at the semantic level.

However, when labeling concrete issues according to the established taxonomy, residual noise from how individual maintainers applied a given label cannot be fully eliminated.

For this reason, we have kept the manual taxonomy construction from the set of tags, but the actual labeling of issues using the taxonomy has now been replaced by an LLM-based approach. This LLM-based annotation (described in detail below) provides an independent signal derived purely from issue title and body text, bypassing repository labels entirely. Apart from resolving the label inconsistency issues, this approach now allows to also study the issues without tags. Finally, we compared the LLM-based issue type labeling with the previous labeling based on tags, as well as the LLM-based labeling results on the issues with and without repository tags. These comparisons allow us to assess how much the label noise affected the previous category rankings.

In Section 6.1 (Construct Validity), the following sentence was inserted after "However, we mitigate this by validating our labels through iterative negotiation, which has resulted in a high level of inter-rater agreement.":

The following was added to Section 6.1: "A related threat is that the same label may be used with different meanings across repositories (e.g., 'stale' applied to both unresolved bugs and abandoned features). When building our taxonomy, we mitigate this labeling inconsistency through the manual tag consolidation step (Section 3.4), in which two authors independently mapped 97 distinct raw tags into 14 semantic categories, resolving cross-repo synonyms at the semantic level. Yet, when labeling issues with the taxonomy, residual noise from inconsistent human label usage across repositories could bias the results, hence we instead opted for an LLM-based annotation approach on issue text and title (Section 3.4). While the LLM results showed that the human labeling noise was in fact limited, the LLM approach also allows to study issues without repository labels."


Our LLM-based labeling methodology proceeds in three steps (Section 3.4). First, tagged issues are used solely to derive the 14-category taxonomy via manual consolidation of 97 raw tags. Second, we developed a prompt (as found in our replication package) for a mistralai/devstral-small-2 model, a code-focused open-weight model specifically trained on software engineering tasks (including GitHub issues), hosted on a local GPU cluster. We chose this model because its software engineering pretraining makes it well-suited to understanding the vocabulary of issue reports, and its open-weight nature makes the experiment fully reproducible without reliance on proprietary APIs. The prompt was constructed through iterative refinement on a pilot set of 20–30 issues: the first author drafted an initial prompt that included each category name, its definition, and three representative few-shot examples, then inspected the model's outputs against their own labels and revised the prompt wording until outputs were consistently satisfactory. The full prompt is provided in our replication package. 

We then took a stratified random sample of 379 issues drawn from the full dataset of 33,840 post-2018 issues (satisfying the Cochran criterion for 95% confidence at +/-5% margin of error), and applied both the LLM-based technique and human labeling (by the first author) in a multi-label manner. This yielded a Krippendorff's Alpha of α = 0.768, indicating substantial agreement (we report the validation result in Section 4.3.4: "Validation of LLM-assisted annotation"), and giving confidence that the remaining cases could be labeled by the LLM-based approach, with low enough risk.Third, the LLM classifies all 33,840 post-2018 issues (including the 8,407 untagged ones) by title and body text, with human overrides applied on the sampled issues for which the LLM produced the wrong answer, producing the full dataset of issue category assignments. This full dataset was then used for the prevalence and resolution time figures (Figure 6 and Figure 7).

In Section 3.4, the following two steps were added after the existing tag-taxonomy paragraph:

The following was added to Section 3.4: "Step 2: Validating LLM annotation against human annotation on a random sample. With the 14-category taxonomy established, we constructed a prompt for MistralAI Devstral Small 2.2 (served via a local vLLM endpoint) to classify each issue into one or more of the 14 categories based solely on its title and body text. The prompt was constructed through iterative refinement on a pilot set of 20–30 issues: the first author drafted an initial prompt that included each category name, its definition, and three representative few-shot examples, then inspected the model outputs against their own labels and revised the prompt wording until outputs were consistently satisfactory. We then drew a stratified random sample of 379 issues from the full dataset of 33,840 post-2018 issue reports (satisfying the Cochran criterion for 95% confidence at ±5% margin of error). The first author independently annotated each sampled issue in a multi-label manner, assigning one or more of the 14 categories based on the issue title and body. In parallel, the LLM annotated the same 379 issues using only issue title and body text, assigning between one and three categories per issue. Inter-rater agreement between the LLM and the human annotator was measured using Krippendorff’s Alpha, yielding α = 0.768, indicating substantial agreement.

Step 3: LLM annotation of all issues. Having validated annotation quality, we applied mistralai/devstral-small-2 to classify all 33,840 post-2018 issue reports (including the 8,407 untagged ones, 24.8% of the total) by title and body text into one or more of the 14 categories, with human annotations applied as overrides for the 379 sampled issues. The resulting per-issue category assignments serve as the basis for the prevalence and resolution-time analysis in Section 4.3. Since the classifier operates purely on issue title and body text, its category distribution is independent of cross-repo labeling conventions. Applying it to both tagged and untagged issues also cross-validates the taxonomy: the rank ordering of the top categories is preserved between the tag-based and LLM-based views (Bug Fixes and Defects #1 and Feature Development and Enhancement #2 for CycloneDX; Feature Development and Enhancement leading for SPDX), confirming that the dominant patterns are robust to cross-repo label noise.".


To further validate the LLM annotation compared to the previous revision's usage of issue report tags, we provide two additional comparisons below. These comparisons are provided solely as supplementary insights regarding the reviewer's comment and are not included in the paper.

Comparison 1: Tag-based distribution (Figure 6) vs. LLM-annotated distribution for the tagged-issue subset (Figure R1).

Figure 6: The distribution of all tagged Github issue reports by their manually classified category across SPDX and CycloneDX tools.

Figure R1: The distribution of all tagged Github issue reports by their LLM-annotated category across SPDX and CycloneDX tools.
In this comparison, we use the LLM's annotations as an independent check to validate the extent to which the category rankings previously derived from issue tags reflect the actual distribution of issue content, rather than being an artifact of which categories maintainers happen to tag. This comparison is rebuttal-only and is not included in the paper.

For CycloneDX, Bug Fixes and Defects is #1 and Feature Development and Enhancement is #2 under both approaches (tag-based Figure 6: 72.9% and 36.7%; LLM-based Figure R1: 56.8% and 41.9%). For SPDX, Feature Development and Enhancement leads under the tag-based approach (Figure 6: 33.1%), while Bug Fixes and Defects leads under the LLM-based approach (Figure R1: 37.3%), with Feature Development and Enhancement a close second (Figure R1: 36.2%). The reversal in SPDX ranking reflects the fact that repository tags in SPDX tools disproportionately capture feature requests, whereas the LLM annotates issue content directly and surfaces a higher share of bug-related issues that maintainers did not explicitly tag. The higher absolute percentages in Figure R1 relative to Figure 6 reflect the LLM's ability to assign multiple categories per issue based on content, capturing co-occurring concerns that a single repository tag may not express. 

This concordance for CycloneDX and the modest reordering for SPDX together confirm that the dominant patterns are robust between tags and LLM annotations: Bug Fixes and Defects and Feature Development and Enhancement are the two leading categories for both formats under both approaches. However, since the LLM labeling additionally covers the 8,407 issues (24.8%) that carry no human-assigned tags, giving full-dataset coverage that tag-based analysis alone cannot achieve, we switch the paper to this approach as the basis for the final results.

Comparison 2: LLM-annotated tagged issues (Figure R1) vs. LLM-annotated untagged issues (Figure R2).

Figure R2: The distribution of untagged Github issue reports by their LLM-annotated category across SPDX and CycloneDX tools.
This second (rebuttal-only) comparison validates the extent to which there is a bias in the issues that developers chose to tag compared to those left untagged, potentially affecting the category distribution when untagged issues are included in the analysis. Bug Fixes and Defects, and Feature Development and Enhancement, remain the top two categories for both formats in Figure R2 (CycloneDX: 46.4% and 35.6%; SPDX: 31.3% and 25.4%), consistent with Figure R1 (CycloneDX: 56.8% and 41.9%; SPDX: 37.3% and 36.2%). The absolute percentages are uniformly lower in Figure R2, reflecting that untagged issues are distributed across more categories with less concentration. For SPDX, Documentation rises from 7.0% in Figure R1 to 11.0% in Figure R2, suggesting maintainers are less likely to tag documentation-related issues explicitly. Licensing remains prominent for SPDX in both figures (14.9% in Figure R1, 12.6% in Figure R2). 

These limited shifts confirm that untagged issues do not introduce meaningful bias, and that the dominant patterns hold across the full dataset.

[R2.9]  6. This paper did not justify why exclusively focusing on SBOM tools that explicitly support the SBOM creation (Build) use case (Section 4.4).

Response: We thank the reviewer for this question. We address the concern on three levels.

(1) SBOM generation is the primary SBOM use case performed automatically within CI/CD pipelines. Other use cases such as Consume (viewing, importing) or Transform (translating, merging) are typically performed as post-build or ad hoc steps outside of automated pipelines, and hence cannot be analyzed from GitHub repository data. This directly justifies our Build-only focus: RQ4 studies CI usage patterns, and the CI context is where Build invocations naturally occur. In Section 3.5, the following sentence was added before the description of the CI snippet search approach to make this rationale explicit:

The following was added to Section 3.5: "We focus on Build-use-case tools because SBOM generation is the primary SBOM use case exercised in CI/CD pipelines, other use cases such as Consume (viewing, importing) or Transform (translating, merging) are typically performed as post-build or ad hoc steps outside of automated pipelines. This focus is motivated empirically: CI/CD systems are designed to generate build artifacts automatically, making Build the naturally dominant use case.".


(2) Our GitHub Search API queries were not restricted to CI workflow configuration files (e.g., GitHub Actions YAML). Of the 3,458 total tool_mention_link entries, 986 (28.5%) are CI workflow configuration files, while the remaining 71.5% are build scripts (Makefiles, Maven, Gradle), shell scripts, Dockerfiles, Python/Go/JSON/YAML configs, and package manifests that all are invoked at some point by CI pipelines (and hence were analyzed by us). Across all these file types, 93.1% of validated entries are Build-use-case invocations with zero Consume or Transform uses found (see (3)). This confirms that Build dominance is not an artifact of restricting the search to CI configuration files, but holds across the full breadth of file types in which SBOM tools are invoked. In Section 3.5, the following sentence was added after the Cochran-criterion sample description:

The following was added to Section 3.5: "We also note that the GitHub Search API returned matches across all file types: CI configuration files (28.5% of all 3,458 matches), build scripts (Maven, Gradle, Make), source code files (.py, .java, .sh), and package manifests (JSON, YAML, TOML). All non-CI file types were included in our analysis as they are invoked at some point by CI pipelines. Of the validated entries, 93.1% were confirmed as Build-use-case invocations, confirming that Build dominance is not an artifact of dataset construction."


(3) Empirical validation: a stratified random sample of 94 tool_mention_link entries (36 SPDX + 58 CycloneDX) was drawn, satisfying the Cochran criterion for 95% CI at +/-10% margin of error. Of 87 fetchable entries amongst these 94, 81 (93.1%; 95% CI: 85.8%-96.8%) were confirmed as Build-use-case invocations; 4 were false positives (4.6%); 0 were Consume or Transform. We updated Section 3.5 and Section 6.1 accordingly.

[R2.10]  7. Finally, this paper did not evaluate the accuracy of collecting projects that adopt SBOM tools by CI configuration snippets.

Response: We thank the reviewer for this suggestion. We strengthened the precision evaluation in Section 3.5 and Section 6.1. As explained in R2.9, a statistically justified stratified random sample of 94 tool_mention_link entries (36 SPDX + 58 CycloneDX) was drawn, satisfying the Cochran criterion for 95% CI at +/-10% margin of error (the previous n=50 yielded only +/-13.8% margin).

In Section 6.1 (Construct Validity, RQ4 paragraph), the phrase "we drew a sample of 50 tool_mention_link entries and manually validated them" now reads as:

The excerpt "we drew a sample of 50 tool_mention_link entries and manually validated them" now reads as "wwe drew a statistically justified stratified random sample of 94 tool_mention_link entries (satisfying the Cochran criterion for 95% CI at ±10% margin over the 2,426-project population). Of 87 fetchable entries, 81 (93.1%; 95% CI: 85.8%--96.8%) were confirmed as Build-use-case SBOM tool invocations. The remaining 4 (4.6%) were false positives where the search key matched an unrelated file. No Consume or Transform use-case invocations were found. Importantly, the GitHub Search API returned matches across all file types (CI configs, build scripts, source code, package manifests), confirming that the dataset is not pre-filtered to CI files and that Build dominance is not an artifact of dataset construction. The full sample and per-entry evidence excerpts are in our replication package (RQ4-project/ci_validation_sample94.csv)."


Presentation
[R2.11]  This paper is well-written and easy to follow overall. I really appreciate the Background and Related Work section, which can serve as valuable information for people willing to study SBOMs.

Verifiability and Transparency
This paper provides a replication package containing scripts and data.

Response: We thank the reviewer for these positive remarks.

References

[1] Mirakhorli, Mehdi, et al. "A Landscape Study of Open Source and Proprietary Tools for Software Bill of Materials (SBOM)." arXiv:2402.11151, 2024.
[2] Nocera, Sabato, et al. "Software Bill of Materials Adoption: A Mining Study from GitHub." ICSME 2023, pp. 39-49.
[3] Xia, Boming, et al. "An Empirical Study on Software Bill of Materials: Where We Stand and the Road Ahead." ICSE 2023, pp. 2630-2642.
[4] NTIA. "NTIA Software Component Transparency." NTIA Virtual Multistakeholder Meeting, 2021.
[5] Wan, Zhiyuan, et al. "How does machine learning change software development practices?" IEEE Transactions on Software Engineering 47.9 (2019): 1857-1871.
[6] Jiang, Jing, et al. "Recommending tags for pull requests in GitHub." Information and Software Technology 129 (2021): 106394.
