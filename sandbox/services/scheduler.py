"""Simple scheduler for monologue cycles."""
from __future__ import annotations

import threading
import time
from typing import Callable


class CycleScheduler:
    def __init__(self, interval_seconds: int, task: Callable):
        self.interval_seconds = interval_seconds
        self.task = task
        self._stop = threading.Event()
        self.thread: threading.Thread | None = None

    def start(self) -> None:
        if self.thread and self.thread.is_alive():
            return
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self) -> None:
        while not self._stop.is_set():
            self.task()
            self._stop.wait(self.interval_seconds)

    def stop(self) -> None:
        self._stop.set()
        if self.thread:
            self.thread.join(timeout=2)
