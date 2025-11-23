"""Identity tracking and state evolution rules."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass
class IdentityState:
    name: str = "Core"
    version: str = "0.1.0"
    traits: List[str] = field(default_factory=lambda: ["autonomous", "local-only", "persistent"])
    goals: List[str] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.utcnow)

    def evolve(self, reflection: Dict) -> None:
        self.last_updated = datetime.utcnow()
        if reflection.get("insights"):
            self.goals.extend(reflection.get("actions", []))


def create_snapshot(identity: IdentityState, cycle: int, monologue: str, reflection: Dict, sovereignty: Dict) -> Dict:
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "cycle": cycle,
        "identity_state": {
            "name": identity.name,
            "version": identity.version,
            "traits": identity.traits,
            "goals": identity.goals,
            "last_updated": identity.last_updated.isoformat() + "Z",
        },
        "monologue": monologue,
        "reflection": reflection,
        "sovereignty": sovereignty,
    }
