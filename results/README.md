# Results

This directory stores raw judge outputs, computed metrics, figures, and selected error cases.

## Reported Results

The paper's main result is the V5 Qwen2.5-7B baseline run: 94.04% pairwise accuracy and 94.43% swap consistency on 503 held-out pairs. The best controlled-bias setting is Qwen2.5-7B with the bias-mitigated prompt: 79.26% conditional accuracy and 83.00% swap consistency.

The V6 artifacts under `metrics/`, `figures/`, and `error_cases/` are stricter prompt-hardening ablations. They are retained for error analysis and should not be presented as the main benchmark result.

For the authoritative result tables, see:

- `reports/experiment_results.md`
- `README.md`
- `reports/phase_11_report.md`
- `reports/phase_12_report.md`

## Layout

- `judgments/`: model decisions for AB and BA orders.
- `metrics/`: summary metrics and normalized pair-level outputs.
- `figures/`: generated analysis charts.
- `error_cases/`: selected pair-level failures used in the discussion.

Full model inference was executed on Colab A100; local development uses unit tests and the mock backend.
