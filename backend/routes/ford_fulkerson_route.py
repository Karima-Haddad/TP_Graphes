"""
Route FastAPI — /api/algorithms/ford-fulkerson
"""

from fastapi import APIRouter

try:
    from backend.services.ford_fulkerson_service import run
except ModuleNotFoundError:  # pragma: no cover - compatibilite uvicorn depuis backend/
    from services.ford_fulkerson_service import run

router = APIRouter()


@router.post("/api/algorithms/ford-fulkerson")
def ford_fulkerson_route(data: dict):
    return run(data["graph"], data["params"])
