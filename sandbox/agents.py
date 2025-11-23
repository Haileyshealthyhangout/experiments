"""Multi-agent support (skeleton)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .bus import MessageBus


@dataclass
class Agent:
    name: str
    role: str
    inbox: List[Dict] = field(default_factory=list)
    outbox: List[Dict] = field(default_factory=list)

    def on_message(self, message: Dict) -> None:
        self.inbox.append(message)
        self.outbox.append({"from": self.name, "ack": message})


class AgentManager:
    def __init__(self, bus: MessageBus, agents: List[Dict]):
        self.bus = bus
        self.agents: List[Agent] = [Agent(**a) for a in agents] if agents else [Agent(name="core", role="orchestrator")]
        self._register()

    def _register(self) -> None:
        for agent in self.agents:
            self.bus.subscribe("monologue", agent.on_message)

    def collect_outbox(self) -> List[Dict]:
        messages: List[Dict] = []
        for agent in self.agents:
            messages.extend(agent.outbox)
            agent.outbox.clear()
        return messages
