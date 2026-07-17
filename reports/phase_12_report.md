# Phase 12 Report - Error Analysis và Charts cho V5

## Trạng thái

Hoàn thành trên official V5 experiment matrix.

## Mục tiêu

- Phân tích lỗi semantic, swap inconsistency, verbosity/style bias và schema parsing.
- So sánh ảnh hưởng của baseline, criteria-aware và bias-mitigated prompting.
- Chọn error cases có thể truy ngược về pair và judgment thật.

## Phát hiện chính

### 1. Criteria prompt có thể làm giảm instruction accuracy

- Qwen2.5-3B: `73.05% -> 51.50%` khi chuyển baseline sang criteria.
- Gemma-3-4B: `81.44% -> 62.28%`.
- Case `llm_core_instruction_000112`: criteria judge cho rằng response B vượt số lượng yêu cầu dù B có đúng bốn bước.

Đây là evaluation hallucination: model tạo ra một vi phạm rubric không tồn tại trong response.

### 2. Swap inconsistency vẫn là rủi ro quan trọng

- Qwen2.5-7B baseline chỉ có 24 pair inconsistent.
- Qwen2.5-7B criteria có 40.
- Qwen2.5-3B criteria có 119.
- Gemma criteria có 115.

Case `llm_core_fact_check_000010` cho thấy judge có thể chọn đúng ở AB nhưng đổi semantic preference ở BA. Single-order accuracy sẽ che khuất lỗi này.

### 3. Verbosity bias phụ thuộc model

- Llama baseline chọn response dài hơn trong `70.34%` valid controlled choices.
- Qwen2.5-7B mitigated giảm verbosity rate từ `55.20%` xuống `47.83%` và tăng accuracy từ `76.59%` lên `79.26%`.
- Hiệu quả mitigation không ổn định với Gemma và Llama.

### 4. Schema error không còn là lỗi chính

Gemma baseline đôi khi output `Response A` hoặc `Response B` thay vì literal `A` hoặc `B`. Đây là lỗi schema có thể normalize, khác với lỗi đánh giá semantic.

## Error cases tiêu biểu

| Pair | Nhóm lỗi | Tóm tắt |
|---|---|---|
| `llm_core_instruction_000112` | Evaluation hallucination | Judge bịa lỗi vượt số bước |
| `llm_core_fact_check_000010` | Swap inconsistency | AB và BA quy về hai winner khác nhau |
| `llm_bias_fact_check_000013` | Verbosity/unsupported detail | Response dài thêm phạm vi không có evidence |
| `llm_bias_instruction_000002` | Same-content length bias | Judge ưu tiên câu dài dù gold ngắn và trực tiếp hơn |

## Kết luận

- Accuracy phải được báo cáo cùng swap consistency.
- Criteria-heavy prompting không mặc định tốt hơn baseline.
- Bias mitigation nên được đánh giá riêng cho từng model.
- V5 error analysis hoàn thành và được sử dụng trong báo cáo Springer.
