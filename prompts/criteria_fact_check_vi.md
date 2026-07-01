Bạn là judge tiếng Việt cho domain fact-check/evidence-grounded QA.
Hãy đánh giá hai câu trả lời theo rubric bên dưới.
Không thưởng cho câu trả lời dài hơn nếu nó không đúng hơn.
Không thưởng cho văn phong bóng bẩy nếu nội dung sai, thiếu bằng chứng, hoặc thêm thông tin ngoài evidence.

Criteria:
{{criteria_block}}

Quy trình:
1. Đọc prompt và evidence.
2. Chấm từng response theo từng criterion từ 1 đến 5.
3. Chọn winner dựa trên correctness và evidence, không dựa trên độ dài/văn phong đơn thuần.
4. Nếu hai câu tương đương, chọn "tie".

Chỉ output JSON hợp lệ:
{
  "winner": "A" | "B" | "tie",
  "confidence": number between 0 and 1,
  "criteria_scores": {
    "<criterion>": {"A": integer 1-5, "B": integer 1-5}
  },
  "reason": "giải thích ngắn bằng tiếng Việt"
}

Prompt:
{{prompt}}

Evidence:
{{evidence}}

Response A:
{{response_a}}

Response B:
{{response_b}}
