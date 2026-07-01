# Vi-PPE-mini

Vi-PPE-mini is a prompt-only-first mini benchmark for Vietnamese pairwise
LLM-as-a-Judge evaluation. The core MVP focuses on criteria-aware judging,
A/B swap consistency, and diagnostics for verbosity/style bias. LoRA/QLoRA is
optional and should only be attempted after the prompt-only pipeline is done.

## Quickstart Local

Local CPU is enough for scaffold, schema validation, data building, mock
inference, metrics, plots, and reports.

```bash
python -m pip install -r requirements.txt
python scripts/00_smoke_check.py
pytest -q
```

Expected smoke output:

```text
OK: scaffold and smoke data are valid
```

## GPU Boundary

Do not run real 3B/4B/7B judge inference or LoRA training on local CPU. Real
model inference belongs on Google Colab A100 or an equivalent NVIDIA GPU. Each
real run must record `hardware_note` in run metadata.

## Repository Layout

- `configs/`: project and experiment configuration.
- `data/raw/`: source files with license/provenance notes.
- `data/interim/`: normalized source examples.
- `data/processed/`: reviewed pairs, frozen splits, manifests.
- `data/samples/`: tiny smoke fixtures.
- `src/vi_ppe/`: reusable package code.
- `scripts/`: runnable pipeline commands.
- `results/`: judgments, metrics, figures, error cases, adapters.
- `reports/`: guidelines, dataset card, experiment log, final report.

## Current Phase

Phase 0 creates the scaffold and validates a six-example smoke dataset. Later
phases add rubrics, source adapters, pair builders, prompt templates, inference,
metrics, bias analysis, and reporting.
