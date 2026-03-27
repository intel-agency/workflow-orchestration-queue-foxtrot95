"""
OS-APOW Orchestrator Service

FastAPI application entry point that provides:
- Health and readiness endpoints
- Webhook receiver for GitHub events
- Service orchestration for the Sentinel
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from orchestrator.api.routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown events."""
    # Startup
    print("OS-APOW Orchestrator starting up...")
    yield
    # Shutdown
    print("OS-APOW Orchestrator shutting down...")


app = FastAPI(
    title="OS-APOW Orchestrator",
    description="Orchestrator for Sentinel, Planning, and Orchestration Workflows",
    version="0.1.0",
    lifespan=lifespan,
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint with service information."""
    return {
        "service": "OS-APOW Orchestrator",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


def run() -> None:
    """Entry point for running the FastAPI application."""
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run()
