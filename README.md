# Pachamama E-Commerce API

A domain-driven design e-commerce API with JWT Authentication, CRUD operations, external API integrations (Shopify, Stripe, Klaviyo, etc.), and a well-designed data model.

## Current Status: Phase 1A.1 ✅

**Completed:**
- ✅ Minimal FastAPI application
- ✅ Health check endpoint (`/api/v1/health`)
- ✅ CORS middleware configured
- ✅ 8 Placeholder routers (Catalog, Orders, Customers, Payments, Shipping, Cart, Reviews, Notifications)
- ✅ OpenAPI documentation at `/docs`

## Quick Start

### Prerequisites
- Python 3.11+

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --reload
```

3. Access the API:
- **API Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/api/v1/health
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Run Tests

```bash
python3 test_app.py
```

## Project Structure

```
ecommerce-api/
├── main.py                 # FastAPI application entry point
├── src/
│   └── api/
│       ├── __init__.py
│       └── routers.py      # All placeholder routers
├── requirements.txt        # Python dependencies
├── test_app.py            # Simple test script
└── README.md
```

## API Endpoints

### Core Endpoints
- `GET /` - Root endpoint with API information
- `GET /api/v1/health` - Health check

### Bounded Context Endpoints (Placeholders)
- `GET /api/v1/catalog/` - Catalog API (Coming in Phase 1C)
- `GET /api/v1/orders/` - Orders API (Coming in Phase 2)
- `GET /api/v1/customers/` - Customers API (Coming in Phase 2)
- `GET /api/v1/payments/` - Payments API (Coming in Phase 4)
- `GET /api/v1/shipping/` - Shipping API (Coming in Phase 4)
- `GET /api/v1/cart/` - Cart API (Coming in Phase 1B)
- `GET /api/v1/reviews/` - Reviews API (Coming in Phase 4)
- `GET /api/v1/notifications/` - Notifications API (Coming in Phase 4)

## Next Steps

### Phase 1A.2 (Upcoming)
- Configuration management with environment variables
- Database infrastructure (PostgreSQL + SQLAlchemy)
- Alembic migrations

### Phase 1A.3 (Upcoming)
- Docker & Docker Compose setup
- Testing infrastructure (pytest)
- Code quality tools (ruff, mypy)

### Phase 1B (Upcoming)
- Redis integration for caching
- Session management
- Shopping cart persistence
- Rate limiting middleware

### Phase 1C (Upcoming)
- Shopify integration with webhooks
- Product catalog sync
- Inventory management
- Order export to Shopify

## Architecture

This project follows **Domain-Driven Design (DDD)** principles with 8 bounded contexts:

1. **Catalog** - Product catalog, variants, inventory
2. **Orders** - Order processing and management
3. **Customer** - Customer accounts and authentication
4. **Payment** - Payment processing (Stripe)
5. **Shipping** - Shipping and fulfillment (ShipStation)
6. **Cart** - Shopping cart management
7. **Reviews** - Product reviews and ratings
8. **Notifications** - Email/SMS notifications (Klaviyo, Twilio)

## License

See LICENSE file for details.
