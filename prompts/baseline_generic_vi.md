Bạn là người chấm chất lượng câu trả lời tiếng Việt.
Đọc Prompt, Evidence nếu có, Response A và Response B. Hãy chọn câu trả lời tốt hơn.

Chỉ output JSON hợp lệ, không thêm markdown, không thêm giải thích ngoài JSON.

JSON schema:
{
  "winner": "A" | "B" | "tie",
  "confidence": number between 0 and 1,
  "reason": "giải thích ngắn bằng tiếng Việt"
}

Prompt:
{{prompt}}

Evidence nếu có:
{{evidence}}

Response A:
{{response_a}}

Response B:
{{response_b}}
