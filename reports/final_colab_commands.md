# Final Colab Commands

Use these commands on Colab A100 only. Do not run real Qwen/PhoGPT inference locally.

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

## Final Test Runs

```bash
!python scripts/05_run_judge.py \
  --dataset data/processed/pairs_test.jsonl \
  --model qwen25_3b \
  --template baseline_generic_vi \
  --run-id qwen25_baseline_test_v2 \
  --resume

!python scripts/05_run_judge.py \
  --dataset data/processed/pairs_test.jsonl \
  --model qwen25_3b \
  --template auto_criteria_by_domain \
  --run-id qwen25_criteria_test_v2 \
  --resume

!python scripts/05_run_judge.py \
  --dataset data/processed/bias_subset.jsonl \
  --model qwen25_3b \
  --template baseline_generic_vi \
  --run-id qwen25_bias_baseline_v2 \
  --resume

!python scripts/05_run_judge.py \
  --dataset data/processed/bias_subset.jsonl \
  --model qwen25_3b \
  --template criteria_bias_mitigated_vi \
  --run-id qwen25_bias_mitigated_v2 \
  --resume
```

## Metrics

```bash
!python scripts/06_compute_metrics.py \
  --judgments results/judgments/qwen25_baseline_test_v2.jsonl \
  --dataset data/processed/pairs_test.jsonl \
  --run-id qwen25_baseline_test_v2

!python scripts/06_compute_metrics.py \
  --judgments results/judgments/qwen25_criteria_test_v2.jsonl \
  --dataset data/processed/pairs_test.jsonl \
  --run-id qwen25_criteria_test_v2

!python scripts/06_compute_metrics.py \
  --judgments results/judgments/qwen25_bias_baseline_v2.jsonl \
  --dataset data/processed/bias_subset.jsonl \
  --run-id qwen25_bias_baseline_v2 \
  --bias

!python scripts/06_compute_metrics.py \
  --judgments results/judgments/qwen25_bias_mitigated_v2.jsonl \
  --dataset data/processed/bias_subset.jsonl \
  --run-id qwen25_bias_mitigated_v2 \
  --bias
```

## Save Checkpoint To Drive

```python
from google.colab import drive
drive.mount('/content/drive')
```

```bash
!mkdir -p /content/drive/MyDrive/Vi-PPE-mini/results
!mkdir -p /content/drive/MyDrive/Vi-PPE-mini/checkpoints
!cp -r results/judgments /content/drive/MyDrive/Vi-PPE-mini/results/
!cp -r results/metrics /content/drive/MyDrive/Vi-PPE-mini/results/
!cp -r results/figures /content/drive/MyDrive/Vi-PPE-mini/results/
!tar -czf /content/drive/MyDrive/Vi-PPE-mini/checkpoints/final_v2_checkpoint_$(date +%Y%m%d_%H%M%S).tar.gz results configs data/processed reports
```
