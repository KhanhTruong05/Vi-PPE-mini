from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    jsonl_path = Path(path)
    if not jsonl_path.exists():
        raise FileNotFoundError(f"JSONL file not found: {jsonl_path}")

    records: list[dict[str, Any]] = []
    with jsonl_path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON at {jsonl_path}:{line_number}: {exc}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"Expected object at {jsonl_path}:{line_number}")
            records.append(record)
    return records


def write_jsonl(path: str | Path, records: Iterable[dict[str, Any]]) -> None:
    jsonl_path = Path(path)
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    with jsonl_path.open("w", encoding="utf-8", newline="\n") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
            f.write("\n")
