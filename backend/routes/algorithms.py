try:
    from backend.algorithms.euler import run_euler
    from backend.algorithms.welsh_powell import run_welsh_powell
    from backend.models.graph import GraphRequest
except ModuleNotFoundError:  # pragma: no cover - compatibilite uvicorn depuis backend/
    from algorithms.euler import run_euler
    from algorithms.welsh_powell import run_welsh_powell
    from models.graph import GraphRequest

from fastapi import APIRouter


router = APIRouter(prefix="/algorithms", tags=["algorithms"])


@router.post("/welsh-powell")
def welsh_powell_route(graph: GraphRequest):
    return run_welsh_powell(graph)


@router.post("/euler")
def euler_route(graph: GraphRequest):
    return run_euler(graph)
