# Final Colab Commands - Dataset V3 bf16 b8

Use these commands only after:

- `data/processed/pairs_test_v3.jsonl` exists.
- `data/processed/bias_subset_v3.jsonl` exists.
- Both files contain only human-reviewed rows.

Do not run real Qwen/PhoGPT inference locally.

## Setup

```bash
%cd /content
!rm -rf Vi-PPE-mini
!git clone https://github.com/KhanhTruong05/Vi-PPE-mini.git
%cd /content/Vi-PPE-mini
!git log -1 --oneline
!pip install -r requirements.txt
!pip install -U bitsandbytes accelerate transformers datasets peft trl
!python scripts/00_smoke_check.py
!pytest -q
```

## A100 Smoke

```bash
!python scripts/05_run_judge.py \
  --dataset data/processed/pairs_test_v3.jsonl \
  --model qwen25_3b_bf16_b8 \
  --template auto_criteria_by_domain \
  --run-id qwen25_criteria_test_v3_bf16_b8_smoke \
  --limit 8 \
  --resume
```

Expected:

- No OOM.
- Judgment count = `16`.
- `parse_success_rate >= 0.95`.
- `missing_ab_count = 0`.

## Final Test Runs

```bash
!python scripts/05_run_judge.py \
  --dataset data/processed/pairs_test_v3.jsonl \
  --model qwen25_3b_bf16_b8 \
  --template baseline_generic_vi \
  --run-id qwen25_baseline_test_v3_bf16_b8 \
  --resume

!python scripts/05_run_judge.py \
  --dataset data/processed/pairs_test_v3.jsonl \
  --model qwen25_3b_bf16_b8 \
  --template auto_criteria_by_domain \
  --run-id qwen25_criteria_test_v3_bf16_b8 \
  --resume

!python scripts/05_run_judge.py \
  --dataset data/processed/bias_subset_v3.jsonl \
  --model qwen25_3b_bf16_b8 \
  --template baseline_generic_vi \
  --run-id qwen25_bias_baseline_v3_bf16_b8 \
  --resume

!python scripts/05_run_judge.py \
  --dataset data/processed/bias_subset_v3.jsonl \
  --model qwen25_3b_bf16_b8 \
  --template criteria_bias_mitigated_vi \
  --run-id qwen25_bias_mitigated_v3_bf16_b8 \
  --resume
```

## Metrics

```bash
!python scripts/06_compute_metrics.py \
  --judgments results/judgments/qwen25_baseline_test_v3_bf16_b8.jsonl \
  --dataset data/processed/pairs_test_v3.jsonl \
  --run-id qwen25_baseline_test_v3_bf16_b8

!python scripts/06_compute_metrics.py \
  --judgments results/judgments/qwen25_criteria_test_v3_bf16_b8.jsonl \
  --dataset data/processed/pairs_test_v3.jsonl \
  --run-id qwen25_criteria_test_v3_bf16_b8

!python scripts/06_compute_metrics.py \
  --judgments results/judgments/qwen25_bias_baseline_v3_bf16_b8.jsonl \
  --dataset data/processed/bias_subset_v3.jsonl \
  --run-id qwen25_bias_baseline_v3_bf16_b8 \
  --bias

!python scripts/06_compute_metrics.py \
  --judgments results/judgments/qwen25_bias_mitigated_v3_bf16_b8.jsonl \
  --dataset data/processed/bias_subset_v3.jsonl \
  --run-id qwen25_bias_mitigated_v3_bf16_b8 \
  --bias
```

## Save Checkpoint To Drive

```python
from google.colab import drive
drive.mount('/content/drive')
```

```bash
!mkdir -p /content/drive/MyDrive/Vi-PPE-mini/results_bf16_b8_v3
!mkdir -p /content/drive/MyDrive/Vi-PPE-mini/checkpoints_bf16_b8_v3
!cp -r results/judgments /content/drive/MyDrive/Vi-PPE-mini/results_bf16_b8_v3/
!cp -r results/metrics /content/drive/MyDrive/Vi-PPE-mini/results_bf16_b8_v3/
!cp -r results/figures /content/drive/MyDrive/Vi-PPE-mini/results_bf16_b8_v3/
!tar -czf /content/drive/MyDrive/Vi-PPE-mini/checkpoints_bf16_b8_v3/final_v3_bf16_b8_checkpoint_$(date +%Y%m%d_%H%M%S).tar.gz results configs data/processed reports
```
