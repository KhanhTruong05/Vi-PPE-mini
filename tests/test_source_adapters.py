from vi_ppe.data_sources import build_adapter
from vi_ppe.io import read_jsonl
from vi_ppe.schemas import validate_source_items


def test_configured_jsonl_adapters_normalize_rows():
    sources = {
        "viquad": "data/raw/viquad_sample.jsonl",
        "vifactcheck": "data/raw/vifactcheck_sample.jsonl",
        "vihsd": "data/raw/vihsd_sample.jsonl",
    }
    items = []
    for name, path in sources.items():
        adapter = build_adapter(name)
        items.extend(adapter.iter_normalized(path, limit=2))
    assert len(items) == 6
    validate_source_items(items)
    assert all(item["source_dataset"] for item in items)
    assert all(item["license_note"] for item in items)


def test_built_sources_artifact_is_valid_if_present():
    items = read_jsonl("data/interim/prompts_raw.jsonl")
    validate_source_items(items)
