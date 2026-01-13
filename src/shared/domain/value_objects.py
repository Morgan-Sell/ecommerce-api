"""Shared value objects for domain models.

Value Objects are immutable objects that represent a descriptive aspect of the domain
with no conceptual identity. They are defined by their attributes.
"""

import re
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    """Money value object with amount and currency.

    Immutable representation of money with currency.

    Example:
        >>> price = Money(Decimal("29.99"), "USD")
        >>> total = price.add(Money(Decimal("5.00"), "USD"))
        >>> print(total)  # Money(amount=Decimal('34.99'), currency='USD')
    """

    amount: Decimal
    currency: str = "USD"

    def __post_init__(self) -> None:
        """Validate money value after initialization."""
        if self.amount < 0:
            raise ValueError(f"Amount cannot be negative: {self.amount}")
        if not self.currency or len(self.currency) != 3:
            raise ValueError(
                f"Currency must be 3-letter ISO code, got: {self.currency}"
            )

    def add(self, other: "Money") -> "Money":
        """Add two Money objects with same currency."""
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot add money with different currencies: "
                f"{self.currency} and {other.currency}"
            )
        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: "Money") -> "Money":
        """Subtract two Money objects with same currency."""
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot subtract money with different currencies: "
                f"{self.currency} and {other.currency}"
            )
        return Money(self.amount - other.amount, self.currency)

    def multiply(self, factor: int | float) -> "Money":
        """Multiply money by a factor."""
        return Money(self.amount * Decimal(str(factor)), self.currency)

    def __str__(self) -> str:
        """String representation of money."""
        return f"{self.currency} {self.amount:.2f}"


@dataclass(frozen=True)
class Email:
    """Email value object with validation.

    Immutable email address with format validation.

    Example:
        >>> email = Email("customer@pachamama.com")
        >>> print(email)  # customer@pachamama.com
    """

    value: str

    def __post_init__(self) -> None:
        """Validate email format after initialization."""
        # Simple email validation pattern
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, self.value):
            raise ValueError(f"Invalid email format: {self.value}")

    def __str__(self) -> str:
        """String representation of email."""
        return self.value

    @property
    def domain(self) -> str:
        """Get domain part of email."""
        return self.value.split("@")[1]

    @property
    def local_part(self) -> str:
        """Get local part of email (before @)."""
        return self.value.split("@")[0]
