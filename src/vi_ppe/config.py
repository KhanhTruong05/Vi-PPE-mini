from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_project_config(path: str | Path = "configs/project.yaml") -> dict[str, Any]:
    """Load the project YAML config."""
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Config file must contain a YAML mapping: {config_path}")
    return data
