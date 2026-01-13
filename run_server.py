"""Simple script to run the Pachamama API server."""

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Pachamama API...")
    print("📚 Docs available at: http://localhost:8000/docs")
    print("🔍 Health check at: http://localhost:8000/api/v1/health")
    print("\nPress CTRL+C to stop the server\n")

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
