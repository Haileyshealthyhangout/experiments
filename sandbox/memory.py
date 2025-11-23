"""Persistent memory storage abstractions."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List


class MemoryStore:
    def append(self, entry: Dict[str, Any]) -> None:
        raise NotImplementedError

    def load_all(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def latest(self) -> Dict[str, Any] | None:
        items = self.load_all()
        return items[-1] if items else None


class JsonMemoryStore(MemoryStore):
    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text("[]", encoding="utf-8")

    def append(self, entry: Dict[str, Any]) -> None:
        data = self.load_all()
        data.append(entry)
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load_all(self) -> List[Dict[str, Any]]:
        return json.loads(self.path.read_text(encoding="utf-8"))


class SQLiteMemoryStore(MemoryStore):
    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    payload TEXT
                )
                """
            )

    def append(self, entry: Dict[str, Any]) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                "INSERT INTO memory (timestamp, payload) VALUES (?, ?)",
                (entry.get("timestamp"), json.dumps(entry)),
            )

    def load_all(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.execute("SELECT payload FROM memory ORDER BY id ASC")
            return [json.loads(row[0]) for row in cursor.fetchall()]


def create_memory_store(backend: str, data_dir: Path) -> MemoryStore:
    if backend == "json":
        return JsonMemoryStore(data_dir / "memory.json")
    if backend == "sqlite":
        return SQLiteMemoryStore(data_dir / "memory.db")
    raise ValueError(f"Unsupported memory backend: {backend}")
