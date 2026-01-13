"""Custom domain exceptions for Pachamama API.

These exceptions represent domain-level errors that can occur during
business logic execution. They are separate from infrastructure errors
(database, network, etc.).
"""


class DomainException(Exception):
    """Base exception for all domain-related errors.

    All custom domain exceptions should inherit from this class.
    This allows catching all domain errors with a single except clause.
    """

    pass


class EntityNotFoundException(DomainException):
    """Raised when a requested entity cannot be found.

    Example:
        >>> raise EntityNotFoundException("Product", "123e4567-e89b-12d3-a456-426614174000")
        EntityNotFoundException: Product with id 123e4567-e89b-12d3-a456-426614174000 not found
    """

    def __init__(self, entity_type: str, entity_id: str) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} with id {entity_id} not found")


class ValidationException(DomainException):
    """Raised when domain validation rules are violated.

    Example:
        >>> raise ValidationException("Email address must be valid")
        ValidationException: Email address must be valid
    """

    pass


class AuthenticationException(DomainException):
    """Raised when authentication fails.

    Example:
        >>> raise AuthenticationException("Invalid credentials")
        AuthenticationException: Invalid credentials
    """

    pass


class AuthorizationException(DomainException):
    """Raised when user lacks permission for an operation.

    Example:
        >>> raise AuthorizationException("User cannot delete this resource")
        AuthorizationException: User cannot delete this resource
    """

    pass


class BusinessRuleViolationException(DomainException):
    """Raised when a business rule is violated.

    Business rules are domain-specific constraints that go beyond simple
    validation (e.g., "Cannot cancel order after it's been shipped").

    Example:
        >>> raise BusinessRuleViolationException("Cannot apply discount to already discounted items")
        BusinessRuleViolationException: Cannot apply discount to already discounted items
    """

    pass
