import asyncio
from typing import Any, Callable, Dict

class EventBus:
    """Async event bus for loose coupling between engines."""
    def __init__(self):
        self.subscribers: Dict[str, list[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    async def publish(self, event_type: str, data: Any):
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                await callback(data)

event_bus = EventBus()