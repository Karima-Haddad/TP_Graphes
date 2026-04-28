try:
    from backend.algorithms.euler import run_euler
    from backend.algorithms.welsh_powell import run_welsh_powell
    from backend.algorithms.connected_components import run_connected_components
    from backend.algorithms.strongly_connected_components import run_strongly_connected_components
    from backend.models.graph import GraphRequest
except ModuleNotFoundError:  # pragma: no cover - compatibilite uvicorn depuis backend/
    from algorithms.euler import run_euler
    from algorithms.welsh_powell import run_welsh_powell
    from algorithms.connected_components import run_connected_components
    from algorithms.strongly_connected_components import run_strongly_connected_components
    from models.graph import GraphRequest

from fastapi import APIRouter


router = APIRouter(prefix="/algorithms", tags=["algorithms"])


@router.post("/welsh-powell")
def welsh_powell_route(graph: GraphRequest):
    return run_welsh_powell(graph)


@router.post("/euler")
def euler_route(graph: GraphRequest):
    return run_euler(graph)


@router.post("/connected-components")
def connected_components_route(graph: GraphRequest):
    return run_connected_components(graph)


@router.post("/strongly-connected-components")
def strongly_connected_components_route(graph: GraphRequest):
    return run_strongly_connected_components(graph)
