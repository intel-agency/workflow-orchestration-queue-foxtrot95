"""API routes for the orchestrator service."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "OS-APOW Orchestrator"}


@router.get("/ready")
async def readiness() -> dict[str, str]:
    """Readiness check endpoint."""
    return {"status": "ready", "service": "OS-APOW Orchestrator"}
