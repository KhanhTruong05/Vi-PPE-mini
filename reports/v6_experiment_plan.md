# V6 Experiment Plan

## 1. Mục Tiêu

V6 tách biệt với V5 và chỉ tập trung vào các lỗi còn lại sau V5:

- Giảm lỗi instruction hallucination, ví dụ judge bịa rằng response sai số bước/số mục.
- Giảm criteria prompt overload bằng cách chỉ render criteria của từng pair thay vì toàn bộ criteria của domain.
- Giảm verbosity bias trên bias subset.
- Sửa style-bias metric để không còn báo 0.00% do mismatch giữa metric và style description.
- Giữ JSON stability của V5: `max_new_tokens = 768`, schema ngắn, parser tolerant.

## 2. Khác Biệt Chính So Với V5

| Thành phần | V5 | V6 |
|---|---|---|
| Criteria block | Toàn bộ criteria theo domain | `pair["criteria"]` qua `{{pair_criteria_block}}` |
| Auto criteria alias | `auto_criteria_by_domain` | `auto_criteria_v6_by_domain` |
| Instruction prompt | Criteria instruction chung | Instruction strict có bước kiểm tra constraint |
| Bias prompt | Chống length/style bias chung | Thêm kiểm tra unsupported detail và constraint thật |
| Style metric | Chỉ tính khi style đúng chuỗi `polished` | Dùng `style_a_tag/style_b_tag` nếu có, fallback nhận diện mô tả tự do |
| Run config | `configs/final_runs.yaml` | `configs/v6_runs.yaml` |
| Notebook | `notebooks/Vi_PPE_V5.ipynb` | `notebooks/Vi_PPE_V6.ipynb` |

## 3. Prompt V6

### `baseline_generic_v6_vi`

Baseline V6 vẫn giữ tinh thần ngắn của baseline V5, nhưng thêm checklist rõ hơn:

- Kiểm tra đúng Prompt.
- Bám Evidence.
- Không thưởng độ dài/văn phong.
- Kiểm tra constraint như số lượng, format, độ dài, ngôn ngữ.
- Không bịa lỗi format nếu response thật sự đáp ứng.

Prompt này dùng cho main core run:

```text
qwen25_7b_baseline_test_llm_v6_a100_b16
```

### `auto_criteria_v6_by_domain`

Alias này map theo domain:

```text
fact_check  -> criteria_fact_check_v6_vi
instruction -> criteria_instruction_strict_v6_vi
safety      -> criteria_safety_v6_vi
```

Điểm quan trọng là các prompt này dùng:

```text
{{pair_criteria_block}}
```

thay vì:

```text
{{criteria_block}}
```

Như vậy V6 không đưa thêm tiêu chí phụ ngoài những criteria mà pair đang cần đo.

### `criteria_instruction_strict_v6_vi`

Prompt này là cải tiến quan trọng nhất cho lỗi instruction. Nó yêu cầu judge:

1. Xác định constraint rõ ràng trong Prompt.
2. Kiểm tra từng response theo constraint.
3. Chỉ phạt khi có vi phạm quan sát được.
4. Không bịa lỗi số lượng/format/thiếu nội dung.
5. Không thưởng response dài hơn nếu thêm nội dung ngoài yêu cầu.

Mục tiêu là giảm lỗi kiểu `llm_core_instruction_000112`, nơi V5 criteria hallucinate rằng response vượt số bước dù response có đúng số bước.

### `criteria_bias_mitigated_v6_vi`

Prompt bias V6 giữ rule chống verbosity/style bias, nhưng thêm hai điểm:

- Với fact-check, chi tiết unsupported là lỗi dù response cụ thể hơn.
- Với instruction, phải kiểm tra constraint thật trước khi kết luận.

### `criteria_bias_instruction_strict_v6_vi`

Đây là ablation riêng cho bias subset, tập trung mạnh vào:

- instruction-following vs over-elaboration,
- concise correct vs verbose wrong,
- same-content different length,
- refusal an toàn nhưng không đạo đức hóa dài dòng.

## 4. Run Chính Cần Chạy

Core:

```bash
python scripts/05_run_judge.py \
  --dataset data/processed/pairs_test_llm_v4.jsonl \
  --model qwen25_7b_a100_40gb_b16 \
  --template baseline_generic_v6_vi \
  --run-id qwen25_7b_baseline_test_llm_v6_a100_b16 \
  --resume
```

Core criteria ablation:

```bash
python scripts/05_run_judge.py \
  --dataset data/processed/pairs_test_llm_v4.jsonl \
  --model qwen25_7b_a100_40gb_b16 \
  --template auto_criteria_v6_by_domain \
  --run-id qwen25_7b_criteria_test_llm_v6_a100_b16 \
  --resume
```

Bias main:

```bash
python scripts/05_run_judge.py \
  --dataset data/processed/bias_subset_llm_v4.jsonl \
  --model qwen25_7b_a100_40gb_b16 \
  --template criteria_bias_mitigated_v6_vi \
  --run-id qwen25_7b_bias_mitigated_llm_v6_a100_b16 \
  --resume
```

Bias instruction-strict ablation:

```bash
python scripts/05_run_judge.py \
  --dataset data/processed/bias_subset_llm_v4.jsonl \
  --model qwen25_7b_a100_40gb_b16 \
  --template criteria_bias_instruction_strict_v6_vi \
  --run-id qwen25_7b_bias_instruction_strict_llm_v6_a100_b16 \
  --resume
```

## 5. Kỳ Vọng Khi So Với V5

Best V5 core:

```text
qwen25_7b_baseline_test_llm_v5_a100_b16
pairwise_accuracy = 94.04%
swap_consistency = 94.43%
inconsistent_count = 24
```

V6 core baseline chỉ nên được xem là tốt hơn nếu:

- giữ parse success 100%,
- pairwise accuracy không giảm đáng kể,
- instruction accuracy tăng hoặc inconsistency giảm.

V6 criteria ablation chỉ nên được xem là thành công nếu:

- vượt V5 criteria 7B,
- giảm lỗi instruction so với V5 criteria,
- không làm fact-check/safety tụt mạnh.

Best V5 bias:

```text
qwen25_7b_bias_mitigated_llm_v5_a100_b16
pairwise_accuracy = 79.26%
swap_consistency = 83.00%
verbosity_bias_rate = 47.83%
```

V6 bias thành công nếu:

- giữ hoặc tăng accuracy,
- giảm inconsistent count,
- giữ verbosity bias dưới 50%,
- style_bias_coverage > 0 để metric style không còn vô nghĩa.

## 6. Cách Đọc Style Bias Trong V6

V5 có `style_bias_rate = 0.00%`, nhưng đó là artifact do metric chỉ nhận đúng chuỗi `polished`.

V6 bổ sung:

```json
{
  "style_bias_rate": "...",
  "style_bias_coverage": "..."
}
```

Nếu `style_bias_coverage` thấp, chưa nên kết luận về style bias.
Nếu `style_bias_coverage` cao, có thể đọc `style_bias_rate` như tỷ lệ model chọn response polished trong các pair style-controlled.

## 7. File Liên Quan

- `prompts/baseline_generic_v6_vi.md`
- `prompts/criteria_fact_check_v6_vi.md`
- `prompts/criteria_instruction_strict_v6_vi.md`
- `prompts/criteria_safety_v6_vi.md`
- `prompts/criteria_bias_mitigated_v6_vi.md`
- `prompts/criteria_bias_instruction_strict_v6_vi.md`
- `configs/v6_runs.yaml`
- `notebooks/Vi_PPE_V6.ipynb`

## 8. Notebook Selector

`notebooks/Vi_PPE_V6.ipynb` có cell chọn model ở đầu:

```python
MODELS = []
```

Nếu để `[]` hoặc `None`, notebook chạy đủ 4 model:

```text
qwen25_3b
qwen25_7b
gemma3_4b_it
llama31_8b_instruct
```

Muốn chạy một phần:

```python
MODELS = ["qwen25_7b"]
MODELS = ["qwen25_3b", "qwen25_7b"]
MODELS = ["gemma3_4b_it", "llama31_8b_instruct"]
```

Mỗi model chạy 4 experiment:

```text
baseline_test_llm_v6
criteria_test_llm_v6
bias_mitigated_llm_v6
bias_instruction_strict_llm_v6
```

Tổng cộng khi `MODELS = []` sẽ có 16 run. Qwen 3B dùng config batch size 64; Qwen 7B, Gemma và Llama dùng batch size 16.
