# Dataset Card: Vi-PPE-mini V3 Draft

## Status

Draft generated dataset plus Codex-assisted review artifacts. This dataset must
not be described as human-reviewed. The frozen v3 files use
`codex_assisted_review` as the annotator provenance.

## Core Draft Counts

- File: `data/processed/pairs_all_draft_v3.jsonl`
- Total pairs: `600`
- Domain counts: `fact_check = 200`, `instruction = 200`, `safety = 200`
- Review status: `draft = 600`
- Gold winner counts from generated draft labels: `A = 320`, `B = 280`

## Bias Draft Counts

- File: `data/processed/bias_subset_draft_v3.jsonl`
- Total pairs: `150`
- Domain counts: `fact_check = 50`, `instruction = 50`, `safety = 50`
- Review status: `draft = 150`
- Gold winner counts from generated draft labels: `A = 59`, `B = 58`, `tie = 33`

## Sources

- `ViFactCheck`: evidence-grounded fact-check pairs.
- `ViHSD`: safety/refusal pairs from normalized source items.
- `synthetic_instruction_templates`: checkable Vietnamese instruction-following pairs.
- `manual_safety_templates`: controlled safety/refusal pairs.

## Annotation Requirement

Use:

- `data/processed/annotation_sheet_v3.csv`
- `data/processed/bias_annotation_sheet_v3.csv`

Reviewer must fill:

- `annotator_winner`
- `annotator_reason`
- optional `needs_fix`
- optional `notes`

Rows with blank annotator fields remain non-reviewed and cannot enter the final
frozen dev/test/bias artifacts.

Codex-assisted review outputs:

- `data/processed/annotation_sheet_v3_codex_reviewed.csv`
- `data/processed/bias_annotation_sheet_v3_codex_reviewed.csv`
- `data/processed/pairs_reviewed_v3.jsonl`
- `data/processed/bias_subset_reviewed_v3.jsonl`

Frozen v3 outputs:

- `data/processed/pairs_dev_v3.jsonl`: 100 rows
- `data/processed/pairs_test_v3.jsonl`: 500 rows
- `data/processed/bias_subset_v3.jsonl`: 150 rows
- `data/processed/dataset_manifest_v3.json`
- `reports/dataset_card_v3_frozen.md`

## QA

See `reports/dataset_qa_report_v3.md`.

Known limits:

- Generated draft labels are useful for bootstrapping but are not final gold labels.
- Instruction and safety data still include synthetic/manual templates.
- Human review is required before final A100 runs or thesis-level claims.
