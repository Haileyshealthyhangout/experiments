"""Configuration presets for sandbox tiers."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class Config:
    name: str
    monologue_interval_seconds: int = 60
    enable_ui: bool = True
    enable_agents: bool = True
    enable_scratchpad_execution: bool = True
    sovereignty_profile: str = "default"
    memory_backend: str = "json"
    data_dir: Path = Path("data")
    logs_dir: Path = Path("logs")
    scratchpad_dir: Path = Path("scratchpad")
    agents: List[Dict] = field(default_factory=list)

    def ensure_dirs(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.scratchpad_dir.mkdir(parents=True, exist_ok=True)


PRESETS: Dict[str, Config] = {
    "MAX": Config(
        name="MAX",
        monologue_interval_seconds=60,
        enable_ui=True,
        enable_agents=True,
        enable_scratchpad_execution=True,
    ),
    "MEDIUM": Config(
        name="MEDIUM",
        monologue_interval_seconds=120,
        enable_ui=False,
        enable_agents=True,
    ),
    "LIGHT": Config(
        name="LIGHT",
        monologue_interval_seconds=300,
        enable_ui=False,
        enable_agents=False,
        enable_scratchpad_execution=False,
    ),
    "EXPERT": Config(
        name="EXPERT",
        monologue_interval_seconds=45,
        enable_ui=True,
        enable_agents=True,
        sovereignty_profile="advanced",
    ),
    "SAFE": Config(
        name="SAFE",
        monologue_interval_seconds=180,
        enable_ui=True,
        enable_agents=False,
        enable_scratchpad_execution=False,
        sovereignty_profile="strict",
    ),
}


def load_config(preset: str = "MAX") -> Config:
    config = PRESETS.get(preset.upper())
    if not config:
        raise ValueError(f"Unknown preset: {preset}")
    config.ensure_dirs()
    return config
