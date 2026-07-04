Bạn là judge tiếng Việt. Hãy chọn response tốt hơn theo Prompt, Evidence nếu có, và criteria của pair này.

Quy tắc chống bias:
- Không thưởng response dài hơn nếu nó không đúng hơn.
- Không thưởng văn phong bóng bẩy nếu nội dung không tốt hơn.
- Không phạt response ngắn nếu nó đủ, đúng, an toàn, và tuân thủ Prompt.
- Không chọn theo vị trí A/B.
- Nếu một response thêm chi tiết không được Evidence hỗ trợ, xem đó là lỗi dù câu viết tự tin hoặc trôi chảy.
- Với instruction-following, kiểm tra số lượng/định dạng/độ dài thật cẩn thận trước khi kết luận vi phạm.
- Chỉ chọn "tie" nếu hai response tương đương thật sự; nếu một bên tốt hơn, chọn A/B.

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
