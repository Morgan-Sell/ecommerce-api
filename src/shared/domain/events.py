"""Domain events infrastructure.

Domain events represent something that happened in the domain that you want
other parts of the same domain (in-process) to be aware of.
"""

from abc import ABC
from datetime import UTC, datetime
from typing import Any, Callable
from uuid import UUID, uuid4


class DomainEvent(ABC):
    """Base class for all domain events.

    Domain events are immutable facts that represent something that happened
    in the domain. They have a unique ID and timestamp of when they occurred.

    Example:
        >>> class OrderCreated(DomainEvent):
        ...     def __init__(self, order_id: UUID, customer_id: UUID):
        ...         super().__init__()
        ...         self.order_id = order_id
        ...         self.customer_id = customer_id
    """

    def __init__(self) -> None:
        self.event_id: UUID = uuid4()
        self.occurred_at: datetime = datetime.now(UTC)

    def to_dict(self) -> dict[str, Any]:
        """Convert event to dictionary for serialization."""
        return {
            "event_id": str(self.event_id),
            "event_type": self.__class__.__name__,
            "occurred_at": self.occurred_at.isoformat(),
        }

    def __repr__(self) -> str:
        """String representation of event."""
        return f"{self.__class__.__name__}(event_id={self.event_id})"


class EventBus:
    """Simple in-memory event bus for domain events.

    Provides publish/subscribe pattern for domain events within the application.
    This is a simple implementation for in-process event handling.

    Example:
        >>> bus = EventBus()
        >>> def handle_order_created(event):
        ...     print(f"Order {event.order_id} was created!")
        >>> bus.subscribe("OrderCreated", handle_order_created)
        >>> bus.publish(OrderCreated(...))
    """

    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable[[DomainEvent], None]]] = {}

    def subscribe(
        self, event_type: str, handler: Callable[[DomainEvent], None]
    ) -> None:
        """Subscribe a handler to an event type.

        Args:
            event_type: Name of the event class (e.g., "OrderCreated")
            handler: Callable that takes the event as argument
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def unsubscribe(
        self, event_type: str, handler: Callable[[DomainEvent], None]
    ) -> None:
        """Unsubscribe a handler from an event type.

        Args:
            event_type: Name of the event class
            handler: The handler to remove
        """
        if event_type in self._handlers:
            self._handlers[event_type].remove(handler)
            if not self._handlers[event_type]:
                del self._handlers[event_type]

    def publish(self, event: DomainEvent) -> None:
        """Publish an event to all subscribed handlers.

        Args:
            event: The domain event to publish
        """
        event_type = event.__class__.__name__
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                handler(event)

    def clear(self) -> None:
        """Clear all event handlers. Useful for testing."""
        self._handlers.clear()

    def has_subscribers(self, event_type: str) -> bool:
        """Check if an event type has any subscribers."""
        return event_type in self._handlers and len(self._handlers[event_type]) > 0


# Global event bus instance for application-wide use
event_bus = EventBus()
