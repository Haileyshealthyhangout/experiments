"""Internal messaging bus (skeleton)."""
from __future__ import annotations

from collections import defaultdict
from typing import Callable, DefaultDict, List


class MessageBus:
    def __init__(self):
        self.subscribers: DefaultDict[str, List[Callable]] = defaultdict(list)

    def publish(self, topic: str, payload):
        for callback in self.subscribers.get(topic, []):
            callback(payload)

    def subscribe(self, topic: str, callback: Callable):
        self.subscribers[topic].append(callback)
