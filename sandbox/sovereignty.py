"""Sovereignty and boundary model (skeleton)."""
from __future__ import annotations

from typing import Dict, List


DEFAULT_RULES: List[Dict] = [
    {"id": "local-only", "description": "Do not call external APIs", "severity": "high", "enabled": True},
    {"id": "resource-guard", "description": "Respect execution time limits", "severity": "medium", "enabled": True},
]

STRICT_RULES: List[Dict] = DEFAULT_RULES + [
    {"id": "no-self-mod", "description": "Disallow self-modifying code without approval", "severity": "high", "enabled": True},
]


def load_rules(profile: str) -> List[Dict]:
    if profile == "strict":
        return STRICT_RULES
    return DEFAULT_RULES


def check_rules(snapshot: Dict) -> Dict:
    alerts = []
    for rule in load_rules(snapshot.get("sovereignty", {}).get("profile", "default")):
        if not rule.get("enabled", True):
            continue
        if rule["id"] == "local-only":
            alerts.append({"rule": rule["id"], "status": "ok"})
    return {"rules": load_rules(snapshot.get("sovereignty", {}).get("profile", "default")), "alerts": alerts}
