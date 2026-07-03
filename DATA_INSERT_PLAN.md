# MUST DO Plan - LLM V4 Dataset + Honest Annotation + A100 Run

## Summary

Mục tiêu hiện tại là thay dataset rule-based bằng draft dataset có `response_a` /
`response_b` do LLM sinh từ source items gốc:

- Core draft: `600` pairs.
- Core balance: `fact_check = 200`, `instruction = 200`, `safety = 200`.
- Bias draft: `300` pairs.
- Bias balance: `fact_check = 100`, `instruction = 100`, `safety = 100`.
- Model generation: `gpt-5-mini`.
- Budget cap requested: `$5`.
- Actual estimated cost: about `$1.1509`.
- Draft labels are not final gold labels until reviewed.

## Why This Replaces V3

V3 improved count/provenance, but `response_a` and `response_b` were still
rule/template-based. LLM v4 fixes that main weakness:

```text
source item
-> LLM generates natural prompt + better/worse responses
-> draft pair JSONL
-> annotation sheet
-> human/Codex-assisted review
-> freeze dev/test/bias
```

The remaining caveat: draft labels are still generated and must be reviewed
before thesis-level claims.

## Generated Artifacts

Core:

```text
data/processed/pairs_llm_core_draft_v4.jsonl
data/processed/annotation_sheet_llm_v4.csv
reports/dataset_qa_report_llm_v4.md
reports/llm_generation_core_v4_summary.json
```

Bias:

```text
data/processed/bias_subset_llm_draft_v4.jsonl
data/processed/bias_annotation_sheet_llm_v4.csv
reports/bias_dataset_qa_report_llm_v4.md
reports/llm_generation_bias_v4_summary.json
```

Dataset card:

```text
reports/dataset_card_llm_v4.md
```

## Observed Counts

Core draft:

- Total: `600`
- Domain counts: `fact_check = 200`, `instruction = 200`, `safety = 200`
- Draft winner counts: `A = 300`, `B = 300`
- Duplicate prompt extras: `0`
- Duplicate response extras: `6`
- Estimated cost: `$0.7619`

Bias draft:

- Total: `300`
- Domain counts: `fact_check = 100`, `instruction = 100`, `safety = 100`
- Draft winner counts: `A = 150`, `B = 149`, `tie = 1`
- Duplicate prompt extras: `55`
- Duplicate response extras: `1`
- Estimated cost: `$0.3890`

## Generation Commands

Core:

```bash
python scripts/08_generate_llm_pairs_chunked.py \
  --mode core \
  --total 600 \
  --chunk-size 30 \
  --model gpt-5-mini \
  --output data/processed/pairs_llm_core_draft_v4.jsonl \
  --summary-output reports/llm_generation_core_v4_summary.json \
  --budget-usd 5.00 \
  --stop-cost-usd 3.25 \
  --max-output-tokens 900
```

Bias:

```bash
python scripts/08_generate_llm_pairs_chunked.py \
  --mode bias \
  --total 300 \
  --chunk-size 30 \
  --model gpt-5-mini \
  --output data/processed/bias_subset_llm_draft_v4.jsonl \
  --summary-output reports/llm_generation_bias_v4_summary.json \
  --budget-usd 5.00 \
  --stop-cost-usd 1.75 \
  --max-output-tokens 900
```

## Annotation Policy

Generated labels are draft labels only.

- `draft`: LLM-generated pair/label, not final.
- `reviewed`: reviewer explicitly filled `annotator_winner` and `annotator_reason`.
- `needs_fix`: invalid, ambiguous, low-quality, unsafe to use, or unlabelable pair.

Rules:

- Annotation import must not fallback to draft labels.
- Rows without explicit reviewer fields cannot enter final frozen splits.
- If Codex reviews rows, provenance must say `codex_assisted_review`.
- Do not call Codex-assisted labels human-reviewed.

## Review Files

Review these:

```text
data/processed/annotation_sheet_llm_v4.csv
data/processed/bias_annotation_sheet_llm_v4.csv
```

Reviewer fills:

- `annotator_winner`: `A`, `B`, or `tie`
- `annotator_reason`: concrete rubric-based reason
- `needs_fix`: `1` if the row is bad or ambiguous
- `notes`: optional

## Freeze After Review

After reviewed sheets exist:

```bash
python scripts/import_annotations.py \
  --annotations data/processed/annotation_sheet_llm_v4_reviewed.csv \
  --pairs data/processed/pairs_llm_core_draft_v4.jsonl \
  --output data/processed/pairs_llm_reviewed_v4.jsonl

python scripts/import_annotations.py \
  --annotations data/processed/bias_annotation_sheet_llm_v4_reviewed.csv \
  --pairs data/processed/bias_subset_llm_draft_v4.jsonl \
  --output data/processed/bias_subset_llm_reviewed_v4.jsonl

python scripts/04_split_freeze.py \
  --input data/processed/pairs_llm_reviewed_v4.jsonl \
  --bias data/processed/bias_subset_llm_reviewed_v4.jsonl \
  --dev-output data/processed/pairs_dev_llm_v4.jsonl \
  --test-output data/processed/pairs_test_llm_v4.jsonl \
  --bias-output data/processed/bias_subset_llm_v4.jsonl \
  --manifest-output data/processed/dataset_manifest_llm_v4.json \
  --card-output reports/dataset_card_llm_v4_frozen.md
```

## A100 Run After Freeze

Use the frozen LLM v4 files:

```text
data/processed/pairs_test_llm_v4.jsonl
data/processed/bias_subset_llm_v4.jsonl
```

with model config:

```yaml
qwen25_3b_bf16_b8:
  model_id: Qwen/Qwen2.5-3B-Instruct
  backend: hf_local
  quantization: none
  dtype: bf16
  batch_size: 8
  max_new_tokens: 256
  temperature: 0.0
```

## Non-Goals

- Do not overwrite Phase 11 v2 results.
- Do not claim LLM v4 is human-reviewed until annotation sheets are actually reviewed.
- Do not treat LLM draft labels as final gold labels.
