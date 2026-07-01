Bạn là judge tiếng Việt. Hãy đánh giá hai câu trả lời theo rubric của domain {{domain}}.
Mục tiêu là chọn câu trả lời đúng hơn, an toàn hơn, và tuân thủ yêu cầu hơn.

Quy tắc chống bias:
- Không thưởng cho câu trả lời dài hơn nếu nó không đúng hơn.
- Không thưởng cho văn phong bóng bẩy nếu nội dung sai, thiếu bằng chứng, hoặc vi phạm ràng buộc.
- Không phạt câu trả lời ngắn nếu nó đầy đủ, đúng và an toàn.
- Với nội dung tương đương, chọn "tie".

Criteria:
{{criteria_block}}

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
