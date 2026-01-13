"""Tests for domain events."""

from uuid import UUID

import pytest

from src.shared.domain.events import DomainEvent, EventBus


# Create a concrete event for testing
class TestEvent(DomainEvent):
    """Test event with some data."""

    def __init__(self, data: str):
        super().__init__()
        self.data = data


class AnotherTestEvent(DomainEvent):
    """Another test event."""

    def __init__(self, value: int):
        super().__init__()
        self.value = value


class TestDomainEvent:
    """Test suite for DomainEvent."""

    def test_creates_event_with_id(self):
        """Test that event is created with unique ID."""
        event = TestEvent("test")
        assert isinstance(event.event_id, UUID)

    def test_creates_event_with_timestamp(self):
        """Test that event has occurred_at timestamp."""
        event = TestEvent("test")
        assert event.occurred_at is not None

    def test_event_has_unique_ids(self):
        """Test that each event gets unique ID."""
        event1 = TestEvent("test1")
        event2 = TestEvent("test2")
        assert event1.event_id != event2.event_id

    def test_to_dict_includes_event_info(self):
        """Test that to_dict includes basic event info."""
        event = TestEvent("test")
        event_dict = event.to_dict()

        assert "event_id" in event_dict
        assert "event_type" in event_dict
        assert "occurred_at" in event_dict
        assert event_dict["event_type"] == "TestEvent"

    def test_repr(self):
        """Test string representation of event."""
        event = TestEvent("test")
        repr_str = repr(event)

        assert "TestEvent" in repr_str
        assert str(event.event_id) in repr_str


class TestEventBus:
    """Test suite for EventBus."""

    def setup_method(self):
        """Set up fresh event bus for each test."""
        self.bus = EventBus()

    def test_can_subscribe_to_event(self):
        """Test subscribing a handler to an event."""
        called = []

        def handler(event: DomainEvent):
            called.append(event)

        self.bus.subscribe("TestEvent", handler)
        assert self.bus.has_subscribers("TestEvent")

    def test_publish_calls_subscribed_handler(self):
        """Test that publishing calls subscribed handlers."""
        called = []

        def handler(event: DomainEvent):
            called.append(event)

        self.bus.subscribe("TestEvent", handler)
        event = TestEvent("data")
        self.bus.publish(event)

        assert len(called) == 1
        assert called[0] == event

    def test_publish_calls_multiple_handlers(self):
        """Test that multiple handlers are called."""
        call_count = {"count": 0}

        def handler1(event: DomainEvent):
            call_count["count"] += 1

        def handler2(event: DomainEvent):
            call_count["count"] += 10

        self.bus.subscribe("TestEvent", handler1)
        self.bus.subscribe("TestEvent", handler2)
        self.bus.publish(TestEvent("data"))

        assert call_count["count"] == 11

    def test_only_subscribed_event_types_receive_events(self):
        """Test that handlers only receive their subscribed event types."""
        test_called = []
        another_called = []

        def test_handler(event: DomainEvent):
            test_called.append(event)

        def another_handler(event: DomainEvent):
            another_called.append(event)

        self.bus.subscribe("TestEvent", test_handler)
        self.bus.subscribe("AnotherTestEvent", another_handler)

        self.bus.publish(TestEvent("data"))
        self.bus.publish(AnotherTestEvent(42))

        assert len(test_called) == 1
        assert len(another_called) == 1
        assert isinstance(test_called[0], TestEvent)
        assert isinstance(another_called[0], AnotherTestEvent)

    def test_unsubscribe_removes_handler(self):
        """Test that unsubscribe removes a handler."""
        called = []

        def handler(event: DomainEvent):
            called.append(event)

        self.bus.subscribe("TestEvent", handler)
        self.bus.unsubscribe("TestEvent", handler)
        self.bus.publish(TestEvent("data"))

        assert len(called) == 0
        assert not self.bus.has_subscribers("TestEvent")

    def test_clear_removes_all_handlers(self):
        """Test that clear removes all handlers."""

        def handler1(event: DomainEvent):
            pass

        def handler2(event: DomainEvent):
            pass

        self.bus.subscribe("TestEvent", handler1)
        self.bus.subscribe("AnotherTestEvent", handler2)

        self.bus.clear()

        assert not self.bus.has_subscribers("TestEvent")
        assert not self.bus.has_subscribers("AnotherTestEvent")

    def test_has_subscribers_returns_false_for_unknown_event(self):
        """Test has_subscribers returns False for unsubscribed events."""
        assert not self.bus.has_subscribers("UnknownEvent")

    def test_publish_without_subscribers_does_nothing(self):
        """Test that publishing without subscribers doesn't error."""
        # Should not raise any exception
        self.bus.publish(TestEvent("data"))

    def test_handler_receives_correct_event_data(self):
        """Test that handlers receive the correct event data."""
        received_data = []

        def handler(event: TestEvent):
            received_data.append(event.data)

        self.bus.subscribe("TestEvent", handler)
        self.bus.publish(TestEvent("hello"))
        self.bus.publish(TestEvent("world"))

        assert received_data == ["hello", "world"]
