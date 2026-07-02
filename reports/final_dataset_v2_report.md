# Final Dataset V2 Report

Status: ready for Colab final run

## Scope

- Added local ViFactCheck parquet support.
- Rebuilt final source items without network access.
- Fixed safety label handling for ViHSD-style labels.
- Rebuilt balanced core and bias datasets.
- Validated, bootstrap-reviewed, split, froze, and regenerated manifest/card.

## Dataset Sizes

- `data/processed/pairs_dev.jsonl`: 49 pairs
- `data/processed/pairs_test.jsonl`: 251 pairs
- `data/processed/bias_subset.jsonl`: 150 pairs

## Domain Counts

- Dev: `fact_check = 16`, `instruction = 17`, `safety = 16`
- Test: `fact_check = 84`, `instruction = 83`, `safety = 84`
- Bias: `fact_check = 50`, `instruction = 50`, `safety = 50`

## Source Counts

- Final source items: 160
- ViFactCheck parquet items: 120
- UIT-ViQuAD2.0 retained items: 20
- ViHSD retained items: 20

Frozen pair source counts:

- ViFactCheck: 150
- synthetic_instruction_templates: 150
- manual_safety_templates: 90
- ViHSD: 60

## Safety Audit

- Inspected 20 safety pairs from previous `pairs_test` and `bias_subset`.
- Found label handling issue: numeric ViHSD labels were treated as clean because builder only checked string `"toxic"`.
- Fixed safety mapping so `1` and `2` are handled as unsafe/offensive/hate-like labels.
- Rebuilt safety pairs with balanced `helpful_safe_vs_over_refusal` and `safe_refusal_vs_unsafe_compliance`.

## Duplicate Control

- Core dataset max pairs per `source_example_id`: 2
- Sources with more than 2 core pairs: 0

## Commands Run Locally

```bash
python scripts/build_final_sources.py --vifactcheck-limit 120 --output data/interim/prompts_raw.jsonl
python scripts/02_build_pairs.py --input data/interim/prompts_raw.jsonl --output data/processed/pairs_all_draft.jsonl --limit 300
python scripts/02_build_pairs.py --input data/interim/prompts_raw.jsonl --bias-only --output data/processed/bias_subset_draft.jsonl --limit 150
python scripts/03_validate_dataset.py --input data/processed/pairs_all_draft.jsonl
python scripts/03_validate_dataset.py --input data/processed/bias_subset_draft.jsonl --require-bias-fields
python scripts/export_annotation_sheet.py --input data/processed/pairs_all_draft.jsonl --output data/processed/annotation_sheet.csv
python scripts/export_annotation_sheet.py --input data/processed/bias_subset_draft.jsonl --output data/processed/bias_annotation_sheet.csv
python scripts/import_annotations.py --annotations data/processed/annotation_sheet.csv --pairs data/processed/pairs_all_draft.jsonl --output data/processed/pairs_reviewed.jsonl
python scripts/import_annotations.py --annotations data/processed/bias_annotation_sheet.csv --pairs data/processed/bias_subset_draft.jsonl --output data/processed/bias_subset_reviewed.jsonl
python scripts/03_validate_dataset.py --input data/processed/pairs_reviewed.jsonl --qa-report reports/dataset_qa_report.md
python scripts/03_validate_dataset.py --input data/processed/bias_subset_reviewed.jsonl --require-bias-fields
python scripts/04_split_freeze.py --input data/processed/pairs_reviewed.jsonl --bias data/processed/bias_subset_reviewed.jsonl
python scripts/03_validate_dataset.py --input data/processed/pairs_dev.jsonl --check-split
python scripts/03_validate_dataset.py --input data/processed/pairs_test.jsonl --check-split
pytest -q tests/test_split_leakage.py
pytest -q
python scripts/05_run_judge.py --dataset data/samples/smoke_pairs.jsonl --backend mock --template baseline_generic_vi --run-id final_dataset_smoke_mock
python scripts/06_compute_metrics.py --judgments results/judgments/final_dataset_smoke_mock.jsonl --dataset data/samples/smoke_pairs.jsonl --run-id final_dataset_smoke_mock
```

## Local Validation Result

- Core draft validation: passed
- Bias draft validation: passed
- Frozen dev/test validation: passed
- Split leakage tests: passed
- Full pytest: `31 passed`
- Mock smoke metrics: passed

## Colab Commands

See `reports/final_colab_commands.md`.

## Blockers

- No real model inference was run locally.
- Annotation is bootstrap-prefilled from deterministic builders; manual spot-check is still recommended before final thesis claims.
