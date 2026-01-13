"""Tests for custom exceptions."""

import pytest

from src.shared.exceptions import (
    AuthenticationException,
    AuthorizationException,
    BusinessRuleViolationException,
    DomainException,
    EntityNotFoundException,
    ValidationException,
)


class TestDomainException:
    """Test suite for base DomainException."""

    def test_can_raise_domain_exception(self):
        """Test that DomainException can be raised."""
        with pytest.raises(DomainException):
            raise DomainException("Something went wrong")

    def test_domain_exception_is_exception(self):
        """Test that DomainException is an Exception."""
        assert issubclass(DomainException, Exception)

    def test_domain_exception_has_message(self):
        """Test that DomainException stores message."""
        try:
            raise DomainException("Test message")
        except DomainException as e:
            assert str(e) == "Test message"


class TestEntityNotFoundException:
    """Test suite for EntityNotFoundException."""

    def test_raises_with_entity_type_and_id(self):
        """Test raising EntityNotFoundException with entity info."""
        with pytest.raises(EntityNotFoundException) as exc_info:
            raise EntityNotFoundException("Product", "123")

        exception = exc_info.value
        assert exception.entity_type == "Product"
        assert exception.entity_id == "123"

    def test_exception_message_includes_entity_info(self):
        """Test that exception message is descriptive."""
        try:
            raise EntityNotFoundException("Order", "abc-123")
        except EntityNotFoundException as e:
            message = str(e)
            assert "Order" in message
            assert "abc-123" in message
            assert "not found" in message

    def test_is_domain_exception(self):
        """Test that EntityNotFoundException is a DomainException."""
        assert issubclass(EntityNotFoundException, DomainException)

    def test_can_catch_as_domain_exception(self):
        """Test that can be caught as DomainException."""
        with pytest.raises(DomainException):
            raise EntityNotFoundException("Customer", "456")


class TestValidationException:
    """Test suite for ValidationException."""

    def test_can_raise_validation_exception(self):
        """Test raising ValidationException."""
        with pytest.raises(ValidationException):
            raise ValidationException("Invalid email format")

    def test_is_domain_exception(self):
        """Test that ValidationException is a DomainException."""
        assert issubclass(ValidationException, DomainException)

    def test_stores_custom_message(self):
        """Test that custom message is stored."""
        try:
            raise ValidationException("Price must be positive")
        except ValidationException as e:
            assert str(e) == "Price must be positive"


class TestAuthenticationException:
    """Test suite for AuthenticationException."""

    def test_can_raise_authentication_exception(self):
        """Test raising AuthenticationException."""
        with pytest.raises(AuthenticationException):
            raise AuthenticationException("Invalid credentials")

    def test_is_domain_exception(self):
        """Test that AuthenticationException is a DomainException."""
        assert issubclass(AuthenticationException, DomainException)

    def test_stores_message(self):
        """Test that authentication message is stored."""
        try:
            raise AuthenticationException("Token expired")
        except AuthenticationException as e:
            assert str(e) == "Token expired"


class TestAuthorizationException:
    """Test suite for AuthorizationException."""

    def test_can_raise_authorization_exception(self):
        """Test raising AuthorizationException."""
        with pytest.raises(AuthorizationException):
            raise AuthorizationException("Insufficient permissions")

    def test_is_domain_exception(self):
        """Test that AuthorizationException is a DomainException."""
        assert issubclass(AuthorizationException, DomainException)

    def test_stores_message(self):
        """Test that authorization message is stored."""
        try:
            raise AuthorizationException("User cannot delete this resource")
        except AuthorizationException as e:
            assert "User cannot delete this resource" in str(e)


class TestBusinessRuleViolationException:
    """Test suite for BusinessRuleViolationException."""

    def test_can_raise_business_rule_exception(self):
        """Test raising BusinessRuleViolationException."""
        with pytest.raises(BusinessRuleViolationException):
            raise BusinessRuleViolationException("Cannot cancel shipped order")

    def test_is_domain_exception(self):
        """Test that BusinessRuleViolationException is a DomainException."""
        assert issubclass(BusinessRuleViolationException, DomainException)

    def test_stores_message(self):
        """Test that business rule message is stored."""
        try:
            raise BusinessRuleViolationException(
                "Cannot apply discount to already discounted item"
            )
        except BusinessRuleViolationException as e:
            assert "Cannot apply discount" in str(e)


class TestExceptionHierarchy:
    """Test suite for exception hierarchy."""

    def test_all_custom_exceptions_are_domain_exceptions(self):
        """Test that all custom exceptions inherit from DomainException."""
        exceptions = [
            EntityNotFoundException,
            ValidationException,
            AuthenticationException,
            AuthorizationException,
            BusinessRuleViolationException,
        ]

        for exc_class in exceptions:
            assert issubclass(exc_class, DomainException)

    def test_can_catch_all_with_domain_exception(self):
        """Test that catching DomainException catches all custom exceptions."""
        exceptions_to_test = [
            EntityNotFoundException("Product", "123"),
            ValidationException("Invalid"),
            AuthenticationException("Unauthorized"),
            AuthorizationException("Forbidden"),
            BusinessRuleViolationException("Rule violated"),
        ]

        for exception in exceptions_to_test:
            with pytest.raises(DomainException):
                raise exception
