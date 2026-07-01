from __future__ import annotations

from typing import Any

from vi_ppe.data_sources.base import DataSourceAdapter, coalesce, load_jsonl_or_hf, make_source_item, stable_id


class ViQuadAdapter(DataSourceAdapter):
    name = "viquad"
    source_dataset = "UIT-ViQuAD2.0"
    default_license_note = "Hugging Face dataset taidng/UIT-ViQuAD2.0; verify upstream license before redistribution."

    def load_raw(self, input_path_or_hf_id: str | None = None, split: str | None = None):
        if input_path_or_hf_id is None:
            raise ValueError("viquad adapter expects a local JSONL path or Hugging Face dataset id")
        return load_jsonl_or_hf(input_path_or_hf_id, split=split)

    def normalize(self, raw_item: dict[str, Any], index: int = 0) -> dict[str, Any]:
        return make_source_item(
            source_example_id=stable_id("viquad", raw_item, index),
            source_dataset=self.source_dataset,
            domain_candidates=["fact_check"],
            prompt_seed=coalesce(raw_item, ["question", "prompt", "prompt_seed", "question_text"]),
            evidence=coalesce(raw_item, ["context", "passage", "evidence", "paragraph", "article"]),
            gold_answer=coalesce(raw_item, ["answer", "answers", "gold_answer", "answer_text"]),
            source_url=coalesce(raw_item, ["source_url", "url"]),
            license_note=coalesce(raw_item, ["license_note"], self.default_license_note),
            metadata={"adapter": self.name, "row_index": index, "raw_keys": sorted(raw_item.keys())},
        )
