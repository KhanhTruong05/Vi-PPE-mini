# Phase 11 Colab A100 Runbook

Repo dùng trên Colab:

```bash
https://github.com/KhanhTruong05/Vi-PPE-mini.git
```

## 1. Chọn Runtime

Trong Colab:

- Runtime -> Change runtime type
- Hardware accelerator -> GPU
- Ưu tiên A100

Kiểm tra:

```bash
!nvidia-smi
```

Nếu chỉ có T4/L4, chỉ chạy smoke với `--limit 5` hoặc `--limit 20`, không coi là final run.

## 2. Clone Và Install

```bash
%cd /content
!rm -rf Vi-PPE-mini
!git clone https://github.com/KhanhTruong05/Vi-PPE-mini.git
%cd /content/Vi-PPE-mini
!python -m pip install -U pip
!pip install -r requirements.txt
!pip install -U bitsandbytes accelerate transformers datasets peft trl
```

## 3. Kiểm Tra Repo

```bash
!ls -lah data/processed
!python scripts/00_smoke_check.py
!pytest -q
```

Các file cần có:

- `data/processed/pairs_dev.jsonl`
- `data/processed/pairs_test.jsonl`
- `data/processed/bias_subset.jsonl`
- `data/processed/dataset_manifest.json`

Nếu dataset không nằm trong Git, mount Drive rồi copy:

```python
from google.colab import drive
drive.mount('/content/drive')
```

```bash
!mkdir -p data/processed
!cp -r /content/drive/MyDrive/Vi-PPE-mini/data/processed/* data/processed/
```

## 4. Smoke Real Model

Chạy mỗi run 5 pair trước:

```bash
!python scripts/11_colab_phase11_runner.py --limit 5
```

Nếu pass, chạy full.

## 5. Full Phase 11

```bash
!python scripts/11_colab_phase11_runner.py --skip-preflight
```

Script dùng `--resume`, nên nếu Colab disconnect thì chạy lại cùng lệnh.

## 6. Metrics Only

Nếu inference đã xong nhưng cần tính lại metrics:

```bash
!python scripts/11_colab_phase11_runner.py --skip-preflight --skip-inference
```

## 7. Debug Một Run

```bash
!python scripts/11_colab_phase11_runner.py --only-run qwen25_baseline_dev --limit 5
!python scripts/11_colab_phase11_runner.py --only-run qwen25_bias_mitigated --skip-preflight
```

Run IDs chính:

- `qwen25_baseline_dev`
- `qwen25_criteria_dev`
- `qwen25_baseline_test`
- `qwen25_criteria_test`
- `qwen25_bias_baseline`
- `qwen25_bias_mitigated`

## 8. Lưu Kết Quả Về Drive

```python
from google.colab import drive
drive.mount('/content/drive')
```

```bash
!mkdir -p /content/drive/MyDrive/Vi-PPE-mini/results
!cp -r results/judgments /content/drive/MyDrive/Vi-PPE-mini/results/
!cp -r results/metrics /content/drive/MyDrive/Vi-PPE-mini/results/
!cp -r results/figures /content/drive/MyDrive/Vi-PPE-mini/results/
```

Sau khi chạy xong, copy các file này về local để tiếp tục Phase 12:

- `results/judgments/*.jsonl`
- `results/metrics/*.json`
- `results/metrics/*_pair_results.jsonl`
- `results/figures/*.png`
