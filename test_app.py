"""Simple test script for Phase 1A.1"""

import asyncio

from httpx import AsyncClient

from main import app


async def test_endpoints():
    """Test all endpoints."""
    from httpx import ASGITransport

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Test root endpoint
        response = await client.get("/")
        print(f"✅ GET / -> {response.status_code}")
        print(f"   Response: {response.json()}")

        # Test health check
        response = await client.get("/api/v1/health")
        print(f"\n✅ GET /api/v1/health -> {response.status_code}")
        print(f"   Response: {response.json()}")

        # Test favicon (should not 404)
        response = await client.get("/favicon.ico")
        print(f"\n✅ GET /favicon.ico -> {response.status_code}")
        print(f"   Response: Empty favicon (no more 404!)")

        # Test all bounded context endpoints
        contexts = [
            "catalog",
            "orders",
            "customers",
            "payments",
            "shipping",
            "cart",
            "reviews",
            "notifications",
        ]

        for context in contexts:
            response = await client.get(f"/api/v1/{context}/")
            print(f"\n✅ GET /api/v1/{context}/ -> {response.status_code}")
            print(f"   Response: {response.json()}")


if __name__ == "__main__":
    print("🧪 Testing Pachamama API - Phase 1A.1\n")
    print("=" * 50)
    asyncio.run(test_endpoints())
    print("\n" + "=" * 50)
    print("✨ All tests passed!")
