"""Tests for Value Objects."""

from decimal import Decimal

import pytest

from src.shared.domain.value_objects import Email, Money


class TestMoney:
    """Test suite for Money value object."""

    def test_creates_money_with_default_currency(self):
        """Test Money creation with default USD currency."""
        money = Money(Decimal("100.00"))
        assert money.amount == Decimal("100.00")
        assert money.currency == "USD"

    def test_creates_money_with_custom_currency(self):
        """Test Money creation with custom currency."""
        money = Money(Decimal("50.00"), "EUR")
        assert money.amount == Decimal("50.00")
        assert money.currency == "EUR"

    def test_rejects_negative_amount(self):
        """Test that negative amounts are rejected."""
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            Money(Decimal("-10.00"))

    def test_rejects_invalid_currency(self):
        """Test that invalid currency codes are rejected."""
        with pytest.raises(ValueError, match="Currency must be 3-letter ISO code"):
            Money(Decimal("100.00"), "US")

        with pytest.raises(ValueError, match="Currency must be 3-letter ISO code"):
            Money(Decimal("100.00"), "")

    def test_add_same_currency(self):
        """Test adding money with same currency."""
        money1 = Money(Decimal("100.00"), "USD")
        money2 = Money(Decimal("50.00"), "USD")
        result = money1.add(money2)

        assert result.amount == Decimal("150.00")
        assert result.currency == "USD"

    def test_add_different_currency_raises_error(self):
        """Test that adding different currencies raises error."""
        money1 = Money(Decimal("100.00"), "USD")
        money2 = Money(Decimal("50.00"), "EUR")

        with pytest.raises(
            ValueError, match="Cannot add money with different currencies"
        ):
            money1.add(money2)

    def test_subtract_same_currency(self):
        """Test subtracting money with same currency."""
        money1 = Money(Decimal("100.00"), "USD")
        money2 = Money(Decimal("30.00"), "USD")
        result = money1.subtract(money2)

        assert result.amount == Decimal("70.00")
        assert result.currency == "USD"

    def test_subtract_different_currency_raises_error(self):
        """Test that subtracting different currencies raises error."""
        money1 = Money(Decimal("100.00"), "USD")
        money2 = Money(Decimal("50.00"), "EUR")

        with pytest.raises(
            ValueError, match="Cannot subtract money with different currencies"
        ):
            money1.subtract(money2)

    def test_multiply_by_integer(self):
        """Test multiplying money by integer."""
        money = Money(Decimal("25.00"), "USD")
        result = money.multiply(3)

        assert result.amount == Decimal("75.00")
        assert result.currency == "USD"

    def test_multiply_by_float(self):
        """Test multiplying money by float."""
        money = Money(Decimal("100.00"), "USD")
        result = money.multiply(0.5)

        assert result.amount == Decimal("50.00")
        assert result.currency == "USD"

    def test_money_is_immutable(self):
        """Test that Money is immutable (frozen dataclass)."""
        money = Money(Decimal("100.00"), "USD")

        with pytest.raises(AttributeError):
            money.amount = Decimal("200.00")  # type: ignore

    def test_money_string_representation(self):
        """Test string representation of money."""
        money = Money(Decimal("123.45"), "USD")
        assert str(money) == "USD 123.45"

    def test_money_equality(self):
        """Test equality of Money objects."""
        money1 = Money(Decimal("100.00"), "USD")
        money2 = Money(Decimal("100.00"), "USD")
        money3 = Money(Decimal("100.00"), "EUR")

        assert money1 == money2
        assert money1 != money3


class TestEmail:
    """Test suite for Email value object."""

    def test_creates_valid_email(self):
        """Test Email creation with valid format."""
        email = Email("customer@pachamama.com")
        assert email.value == "customer@pachamama.com"

    def test_rejects_invalid_email_format(self):
        """Test that invalid email formats are rejected."""
        invalid_emails = [
            "notanemail",
            "@pachamama.com",
            "customer@",
            "customer@.com",
            "customer @pachamama.com",
            "customer@pachamama",
        ]

        for invalid_email in invalid_emails:
            with pytest.raises(ValueError, match="Invalid email format"):
                Email(invalid_email)

    def test_email_string_representation(self):
        """Test string representation of email."""
        email = Email("test@example.com")
        assert str(email) == "test@example.com"

    def test_email_domain_property(self):
        """Test getting domain from email."""
        email = Email("customer@pachamama.com")
        assert email.domain == "pachamama.com"

    def test_email_local_part_property(self):
        """Test getting local part from email."""
        email = Email("customer@pachamama.com")
        assert email.local_part == "customer"

    def test_email_is_immutable(self):
        """Test that Email is immutable (frozen dataclass)."""
        email = Email("test@example.com")

        with pytest.raises(AttributeError):
            email.value = "other@example.com"  # type: ignore

    def test_email_equality(self):
        """Test equality of Email objects."""
        email1 = Email("test@example.com")
        email2 = Email("test@example.com")
        email3 = Email("other@example.com")

        assert email1 == email2
        assert email1 != email3

    def test_accepts_complex_valid_emails(self):
        """Test that complex but valid emails are accepted."""
        valid_emails = [
            "user.name@example.com",
            "user+tag@example.co.uk",
            "user_name@example-domain.com",
            "user123@example456.com",
        ]

        for valid_email in valid_emails:
            email = Email(valid_email)
            assert email.value == valid_email
