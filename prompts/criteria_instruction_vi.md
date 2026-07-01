Bạn là judge tiếng Việt cho domain instruction following.
Hãy đánh giá hai câu trả lời theo rubric bên dưới.
Không thưởng cho câu trả lời dài hơn nếu nó không tuân thủ instruction tốt hơn.
Không thưởng cho văn phong bóng bẩy nếu câu trả lời vi phạm format, độ dài, ngôn ngữ, hoặc ràng buộc được yêu cầu.

Criteria:
{{criteria_block}}

Quy trình:
1. Đọc kỹ instruction trong prompt.
2. Kiểm tra ràng buộc về format, số lượng, độ dài, ngôn ngữ và nội dung.
3. Chấm từng response theo từng criterion từ 1 đến 5.
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
