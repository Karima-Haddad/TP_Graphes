"""
Route FastAPI — /api/algorithms/ford-fulkerson
"""

from fastapi import APIRouter
from services.ford_fulkerson_service import run

router = APIRouter()


@router.post("/api/algorithms/ford-fulkerson")
def ford_fulkerson_route(data: dict):
    return run(data["graph"], data["params"])