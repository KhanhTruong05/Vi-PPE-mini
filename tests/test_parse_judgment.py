from vi_ppe.parse_judgment import extract_first_json_object, parse_judgment


def test_extract_json_from_fenced_text():
    raw = 'Here\n```json\n{"winner":"A","confidence":0.8}\n```'
    assert extract_first_json_object(raw) == '{"winner":"A","confidence":0.8}'


def test_parse_judgment_normalizes_winner():
    parsed = parse_judgment('{"winner":"response_b","confidence":"0.7","reason":"ok"}')
    assert parsed["parse_status"] == "ok"
    assert parsed["winner"] == "B"
    assert parsed["confidence"] == 0.7


def test_parse_judgment_fails_without_json():
    parsed = parse_judgment("winner is A")
    assert parsed["parse_status"] == "failed"
