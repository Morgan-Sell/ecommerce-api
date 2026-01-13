# AGENTS.md - Developer Guide for AI Coding Agents

This file contains essential information for AI coding agents working on this ecommerce API project.

## Project Overview

Python-based ecommerce API with JWT authentication, CRUD operations, external API integrations, and well-designed data model.

## Build, Lint, and Test Commands

### Setup
```bash
pip install -r requirements.txt  # or: poetry install / uv pip install -r requirements.txt
```

### Testing
```bash
pytest                                              # Run all tests
pytest tests/test_auth.py                           # Run a single test file
pytest tests/test_auth.py::test_jwt_authentication  # Run a specific test function
pytest tests/test_products.py::TestProductCRUD      # Run a specific test class
pytest --cov=. --cov-report=html                    # Run with coverage
pytest -v                                           # Verbose output
pytest -x                                           # Stop on first failure
```

### Linting and Formatting
```bash
ruff check .        # Lint code
ruff check --fix .  # Auto-fix linting issues
ruff format .       # Format code
mypy .              # Type checking
```

### Running the Application
```bash
uvicorn main:app --reload     # FastAPI
flask run --debug             # Flask
python manage.py runserver    # Django
```

## Code Style Guidelines

### Import Organization
Follow PEP 8 import ordering:
```python
# 1. Standard library imports
import os
from typing import List, Optional

# 2. Third-party imports
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

# 3. Local application imports
from app.models import User, Product
from app.auth import get_current_user
```

### Formatting Rules
- Use 4 spaces for indentation (not tabs)
- Maximum line length: 88 characters (Black standard)
- Use trailing commas in multi-line structures
- Two blank lines between top-level functions/classes
- One blank line between methods in a class

### Type Hints
Always use type hints for function signatures:
```python
def get_product(product_id: int) -> Optional[Product]:
    """Retrieve a product by ID."""
    return db.query(Product).filter(Product.id == product_id).first()
```

### Naming Conventions
- **Variables/Functions**: `snake_case` (e.g., `user_id`, `get_product_by_id`)
- **Classes**: `PascalCase` (e.g., `UserModel`, `ProductRepository`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_LOGIN_ATTEMPTS`)
- **Private methods**: Prefix with underscore (e.g., `_validate_token`)
- **Files**: `snake_case.py` (e.g., `auth_service.py`)

### Error Handling
Use appropriate HTTP status codes and always log exceptions:
```python
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

# API error responses
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Product not found"
)

# Exception handling
try:
    result = external_api.fetch_data()
except RequestException as e:
    logger.error(f"External API error: {e}")
    raise HTTPException(status_code=503, detail="Service unavailable")
```

### Data Models
Use Pydantic for request/response validation:
```python
from pydantic import BaseModel, Field
from datetime import datetime

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    created_at: datetime
    
    class Config:
        from_attributes = True  # For SQLAlchemy compatibility
```

### JWT Authentication Pattern
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = os.getenv("SECRET_KEY")  # Use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

### Database Best Practices
- Use SQLAlchemy ORM with Alembic for migrations
- Use context managers for database sessions
- Index frequently queried columns
- Use transactions for multi-step operations

## Testing Guidelines

### Test Structure
```python
import pytest
from httpx import AsyncClient

async def test_create_product(client: AsyncClient, auth_headers: dict):
    """Test product creation with valid data."""
    response = await client.post(
        "/api/products",
        json={"name": "Test Product", "price": 29.99},
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"
```

### Test Coverage Requirements
- Aim for 80%+ code coverage
- Test happy paths and error cases
- Test authentication and authorization flows
- Mock external API calls
- Test input validation

## Additional Guidelines

- **Security**: Never hardcode secrets; use environment variables
- **Documentation**: Add docstrings to all public functions and classes
- **Logging**: Use logging module instead of print statements
- **API Design**: Follow RESTful conventions for endpoints
- **Validation**: Validate all user inputs
- **Architecture**: Use dependency injection for testability
- **Code Quality**: Keep functions small and focused (single responsibility principle)
