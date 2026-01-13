"""Tests for BaseEntity."""

from datetime import datetime
from uuid import UUID

import pytest

from src.shared.domain.base_entity import BaseEntity


class TestBaseEntity:
    """Test suite for BaseEntity."""

    def test_creates_entity_with_auto_generated_id(self):
        """Test that entity creates UUID automatically."""
        entity = BaseEntity()
        assert isinstance(entity.id, UUID)
        assert entity.created_at is not None
        assert entity.updated_at is not None

    def test_creates_entity_with_provided_id(self):
        """Test that entity accepts provided UUID."""
        from uuid import uuid4

        custom_id = uuid4()
        entity = BaseEntity(id=custom_id)
        assert entity.id == custom_id

    def test_creates_entity_with_timestamps(self):
        """Test that entity creates timestamps."""
        from datetime import UTC

        before = datetime.now(UTC)
        entity = BaseEntity()
        after = datetime.now(UTC)

        assert before <= entity.created_at <= after
        assert before <= entity.updated_at <= after

    def test_equality_based_on_id(self):
        """Test that two entities with same ID are equal."""
        from uuid import uuid4

        entity_id = uuid4()
        entity1 = BaseEntity(id=entity_id)
        entity2 = BaseEntity(id=entity_id)

        assert entity1 == entity2

    def test_inequality_with_different_ids(self):
        """Test that entities with different IDs are not equal."""
        entity1 = BaseEntity()
        entity2 = BaseEntity()

        assert entity1 != entity2

    def test_hash_based_on_id(self):
        """Test that hash is based on ID."""
        from uuid import uuid4

        entity_id = uuid4()
        entity1 = BaseEntity(id=entity_id)
        entity2 = BaseEntity(id=entity_id)

        assert hash(entity1) == hash(entity2)

    def test_can_use_entity_in_set(self):
        """Test that entities can be used in sets."""
        from uuid import uuid4

        entity_id = uuid4()
        entity1 = BaseEntity(id=entity_id)
        entity2 = BaseEntity(id=entity_id)
        entity3 = BaseEntity()

        entity_set = {entity1, entity2, entity3}
        assert len(entity_set) == 2  # entity1 and entity2 are same

    def test_repr(self):
        """Test string representation of entity."""
        entity = BaseEntity()
        repr_str = repr(entity)

        assert "BaseEntity" in repr_str
        assert str(entity.id) in repr_str
