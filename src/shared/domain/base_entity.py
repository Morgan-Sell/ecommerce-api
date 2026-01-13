"""Base entity class for all domain entities."""

from datetime import UTC, datetime
from uuid import UUID, uuid4


class BaseEntity:
    """Abstract base entity with common fields for all domain entities.

    Provides:
    - Unique identifier (UUID)
    - Created timestamp
    - Updated timestamp
    - Equality based on ID
    - Hash based on ID
    """

    def __init__(
        self,
        id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        self.id = id or uuid4()
        self.created_at = created_at or datetime.now(UTC)
        self.updated_at = updated_at or datetime.now(UTC)

    def __eq__(self, other: object) -> bool:
        """Two entities are equal if they have the same ID."""
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on entity ID."""
        return hash(self.id)

    def __repr__(self) -> str:
        """String representation of entity."""
        return f"{self.__class__.__name__}(id={self.id})"
