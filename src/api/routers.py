"""Thin placeholder routers for all bounded contexts."""

from fastapi import APIRouter

# Catalog router
catalog_router = APIRouter()


@catalog_router.get("/")
async def catalog_root():
    return {"message": "Catalog API - Coming in Phase 1C"}


# Orders router
orders_router = APIRouter()


@orders_router.get("/")
async def orders_root():
    return {"message": "Orders API - Coming in Phase 2"}


# Customer router
customer_router = APIRouter()


@customer_router.get("/")
async def customer_root():
    return {"message": "Customer API - Coming in Phase 2"}


# Payment router
payment_router = APIRouter()


@payment_router.get("/")
async def payment_root():
    return {"message": "Payment API - Coming in Phase 4"}


# Shipping router
shipping_router = APIRouter()


@shipping_router.get("/")
async def shipping_root():
    return {"message": "Shipping API - Coming in Phase 4"}


# Cart router
cart_router = APIRouter()


@cart_router.get("/")
async def cart_root():
    return {"message": "Cart API - Coming in Phase 1B"}


# Reviews router
reviews_router = APIRouter()


@reviews_router.get("/")
async def reviews_root():
    return {"message": "Reviews API - Coming in Phase 4"}


# Notifications router
notifications_router = APIRouter()


@notifications_router.get("/")
async def notifications_root():
    return {"message": "Notifications API - Coming in Phase 4"}
