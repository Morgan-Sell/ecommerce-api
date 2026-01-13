"""Pachamama API - Minimal FastAPI application for Phase 1A.1"""

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import (
    cart_router,
    catalog_router,
    customer_router,
    notifications_router,
    orders_router,
    payment_router,
    reviews_router,
    shipping_router,
)

# Create FastAPI app
app = FastAPI(
    title="Pachamama API",
    version="v1",
    description="E-Commerce API with Domain-Driven Design",
)

# CORS middleware (optional but configured)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pachamama.com",
        "https://www.pachamama.com",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Pachamama API",
        "version": "v1",
        "phase": "1A.1 - Minimal Setup",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


# Health check endpoint
@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": "Pachamama API",
        "version": "v1",
        "phase": "1A.1",
    }


# Favicon endpoint (prevents 404 errors in browser)
@app.get("/favicon.ico")
async def favicon():
    """Return empty response for favicon to prevent 404."""
    return Response(content="", media_type="image/x-icon")


# Register all routers with /api/v1 prefix
app.include_router(catalog_router, prefix="/api/v1/catalog", tags=["Catalog"])
app.include_router(orders_router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(customer_router, prefix="/api/v1/customers", tags=["Customers"])
app.include_router(payment_router, prefix="/api/v1/payments", tags=["Payments"])
app.include_router(shipping_router, prefix="/api/v1/shipping", tags=["Shipping"])
app.include_router(cart_router, prefix="/api/v1/cart", tags=["Cart"])
app.include_router(reviews_router, prefix="/api/v1/reviews", tags=["Reviews"])
app.include_router(
    notifications_router, prefix="/api/v1/notifications", tags=["Notifications"]
)
