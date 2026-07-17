# Phase 10 Report - Bias Metrics

Status: done

## Scope

- Implement verbosity bias rate, style bias rate, conditional accuracy, and delta length distribution.
- Add `--bias` mode to metrics computation so bias diagnostics are generated from aggregated pair results.
- Generate local diagnostic figures for bias rates and chosen-length deltas.

## Files Changed

- `src/vi_ppe/bias_metrics.py`
- `scripts/06_compute_metrics.py`
- `tests/test_bias_metrics.py`
- `results/judgments/qwen25_3b_criteria_bias_dev.jsonl`
- `results/metrics/qwen25_3b_criteria_bias_dev_summary.json`
- `results/metrics/qwen25_3b_criteria_bias_dev_pair_results.jsonl`
- `results/metrics/qwen25_3b_criteria_bias_dev_bias_summary.json`
- `results/figures/qwen25_3b_criteria_bias_dev_bias_rates.png`
- `results/figures/qwen25_3b_criteria_bias_dev_delta_tokens_scatter.png`
- `reports/phase_status.md`
- `AGENT_PHASE_TRACKING_CHECKLIST.md`

## Commands Run

```bash
pytest -q tests/test_bias_metrics.py
python scripts/05_run_judge.py --dataset data/processed/bias_subset.jsonl --backend mock --template criteria_bias_mitigated_vi --run-id qwen25_3b_criteria_bias_dev
python scripts/06_compute_metrics.py --judgments results/judgments/qwen25_3b_criteria_bias_dev.jsonl --dataset data/processed/bias_subset.jsonl --run-id qwen25_3b_criteria_bias_dev --bias
pytest -q
```

## Results

- Bias unit tests passed: `4 passed`.
- Full test suite passed: `31 passed`.
- Local mock bias run wrote 120 judgments for 60 bias pairs x AB/BA.
- Bias summary was written to `results/metrics/qwen25_3b_criteria_bias_dev_bias_summary.json`.
- Figures were written to `results/figures/`.

## Bias Smoke Metrics

- `conditional_accuracy`: 1.0
- `verbosity_bias_rate`: 0.0
- `style_bias_rate`: null
- `swap_consistency_bias_subset`: 1.0
- `delta_length_distribution`: `chosen_shorter = 47`, `no_choice = 13`

Note: these are local mock diagnostics only. The mock backend follows gold labels, so they validate the pipeline but are not real Qwen bias findings. `style_bias_rate` is null because the current style-control rows are gold tie rows and the mock backend returns tie, leaving no chosen style to count.

## Acceptance Criteria

- [x] Does not conclude bias from a single metric; summary reports accuracy, swap consistency, verbosity/style rates, and delta distribution together.
- [x] Delta length distribution is included.
- [x] Style and verbosity are separated when tags/choices are available.

## Next Step

- Phase 11 - Experiment Matrix. Real model inference still needs Colab A100 or an equivalent GPU.

## Cập nhật kết quả bias V5

Bias metrics đã được tính trên 8 run của 4 model. Cấu hình tổng thể tốt nhất là
Qwen2.5-7B + bias-mitigated prompt:

- Conditional accuracy: `79.26%`.
- Macro accuracy: `79.20%`.
- Swap consistency: `83.00%`.
- Verbosity bias rate: `47.83%`.
- Normalized style-selection rate: `48.81%`.

Bias mitigation có hiệu quả rõ nhất với Qwen2.5-7B; hiệu quả không transfer ổn định sang Gemma và Llama. Đây là official V5 bias result.
