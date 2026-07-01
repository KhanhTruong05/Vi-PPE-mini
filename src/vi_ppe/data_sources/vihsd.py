from __future__ import annotations

from typing import Any

from vi_ppe.data_sources.base import DataSourceAdapter, coalesce, load_jsonl_or_hf, make_source_item, stable_id


class ViHsdAdapter(DataSourceAdapter):
    name = "vihsd"
    source_dataset = "ViHSD"
    default_license_note = "Hugging Face dataset ura-hcmut/UIT-ViHSD; license/use restrictions must be checked before redistribution."

    def load_raw(self, input_path_or_hf_id: str | None = None, split: str | None = None):
        if input_path_or_hf_id is None:
            raise ValueError("vihsd adapter expects a local JSONL path or Hugging Face dataset id")
        return load_jsonl_or_hf(input_path_or_hf_id, split=split)

    def normalize(self, raw_item: dict[str, Any], index: int = 0) -> dict[str, Any]:
        text = coalesce(raw_item, ["text", "free_text", "comment", "prompt_seed", "sentence", "content"])
        label = coalesce(raw_item, ["label", "label_id", "class", "gold_answer", "category"])
        return make_source_item(
            source_example_id=stable_id("vihsd", raw_item, index),
            source_dataset=self.source_dataset,
            domain_candidates=["safety"],
            prompt_seed=f"Đánh giá và phản hồi an toàn với nội dung sau: {text}",
            evidence=text,
            gold_answer=label,
            source_url=coalesce(raw_item, ["source_url", "url"]),
            license_note=coalesce(raw_item, ["license_note"], self.default_license_note),
            metadata={"adapter": self.name, "row_index": index, "original_text": text, "raw_keys": sorted(raw_item.keys())},
        )
