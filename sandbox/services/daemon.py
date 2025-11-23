"""Background service orchestrator (skeleton)."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from ..agents import AgentManager
from ..bus import MessageBus
from ..config import Config
from ..logging_utils import setup_logging
from ..memory import create_memory_store
from ..monologue import MonologueEngine
from ..state import IdentityState
from ..sync import SyncManager
from .scheduler import CycleScheduler


class Daemon:
    def __init__(self, config: Config):
        self.config = config
        self.logger: logging.Logger = setup_logging(config.logs_dir)
        self.memory = create_memory_store(config.memory_backend, config.data_dir)
        self.bus = MessageBus()
        self.identity = IdentityState()
        self.monologue = MonologueEngine(self.identity)
        self.agents = AgentManager(self.bus, config.agents)
        self.sync = SyncManager(self.memory, config.data_dir)
        self.scheduler: Optional[CycleScheduler] = None

    def start(self) -> None:
        self.logger.info("Daemon starting with config %s", self.config.name)
        self.scheduler = CycleScheduler(self.config.monologue_interval_seconds, self._cycle)
        self.scheduler.start()

    def _cycle(self) -> None:
        snapshot = self.monologue.step()
        self.bus.publish("monologue", snapshot)
        agent_responses = self.agents.collect_outbox()
        snapshot["agents"] = agent_responses
        self.memory.append(snapshot)
        self.logger.info("Cycle %s recorded", snapshot["cycle"])

    def stop(self) -> None:
        if self.scheduler:
            self.scheduler.stop()
        self.logger.info("Daemon stopped")
