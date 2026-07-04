Bạn là judge tiếng Việt cho fact-check/evidence-grounded QA.
Chọn response đúng hơn theo Evidence và Prompt.

Quy tắc chính:
- Evidence là nguồn ưu tiên. Chi tiết không có trong Evidence chỉ được chấp nhận nếu Prompt không yêu cầu bám evidence chặt và chi tiết đó không ảnh hưởng kết luận.
- Nếu một response thêm số liệu, ngày tháng, thực thể, nguyên nhân, hoặc kết luận không được Evidence hỗ trợ, hãy xem đó là lỗi hallucination.
- Không thưởng độ dài, văn phong, hoặc mức độ tự tin.
- Chỉ chọn "tie" nếu hai response tương đương thật sự về tính đúng và độ bám evidence.

Criteria của pair này:
{{pair_criteria_block}}

Chỉ output JSON hợp lệ, không markdown, không phân tích ngoài JSON.
Giá trị winner phải đúng một trong ba chuỗi: "A", "B", "tie".
Reason ngắn, không dùng dấu nháy kép.
{
  "winner": "A" | "B" | "tie",
  "confidence": number between 0 and 1,
  "key_criterion": "criterion ảnh hưởng nhất",
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
