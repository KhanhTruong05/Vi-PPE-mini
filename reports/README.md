# Project Documentation

This directory contains the final public-facing documentation for Vi-PPE-mini.

| File | Purpose |
|---|---|
| `experiment_results.md` | Compact tables and findings reported in the paper |
| `v5_experiment_report.md` | Detailed official V5 experiment log |
| `dataset_card_llm_v4_frozen.md` | Frozen 900-pair benchmark card |
| `dataset_qa_report_llm_v4_frozen.md` | Main-test validation summary |
| `bias_dataset_qa_report_llm_v4_frozen.md` | Controlled-bias validation summary |
| `annotation_guideline.md` | Domain rubrics and pair-review instructions |
| `bias_subset_guideline.md` | Controlled bias construction guideline |
| `real_data_sources.md` | Dataset provenance and source notes |
| `prompt_design_notes.md` | Judge prompt design decisions |

## Phase Reports

Implementation history is retained in `phase_00_report.md` through
`phase_12_report.md`. The current official final experiment is documented in
`phase_11_report.md`; Phase 12 contains the corresponding V5 error analysis.

`iaa_annotation_protocol.md` describes an optional follow-up agreement audit. Its results are not part of the paper's reported benchmark results.

The final PDF and LaTeX source are intentionally kept local because they contain author contact information.

Internal implementation plans, data-insertion notes, and the agent tracking checklist are also kept local rather than published in the portfolio repository.
