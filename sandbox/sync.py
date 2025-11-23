"""Manual ChatGPT sync helpers (skeleton)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from .memory import MemoryStore


class SyncManager:
    def __init__(self, memory: MemoryStore, data_dir: Path):
        self.memory = memory
        self.export_path = data_dir / "sync_export.json"
        self.import_path = data_dir / "sync_import.json"

    def export_state(self) -> Path:
        data: List[Dict] = self.memory.load_all()
        self.export_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return self.export_path

    def import_updates(self) -> Dict:
        if not self.import_path.exists():
            return {"status": "no-updates"}
        payload = json.loads(self.import_path.read_text(encoding="utf-8"))
        return payload
