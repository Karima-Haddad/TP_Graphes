from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

try:
    from backend.algorithms.connected_components import connected_components
    from backend.algorithms.strongly_connected_components import strongly_connected_components
    from backend.services.graph_analyzer import GraphAnalyzer
except ModuleNotFoundError:  # pragma: no cover - compatibilite uvicorn depuis backend/
    from algorithms.connected_components import connected_components
    from algorithms.strongly_connected_components import strongly_connected_components
    from services.graph_analyzer import GraphAnalyzer


router = APIRouter(prefix="/api/graph", tags=["Graph"])


class GraphAlgorithmRequest(BaseModel):
    graph: dict[str, Any]


@router.post("/cc")
def cc_route(body: GraphAlgorithmRequest) -> dict[str, Any]:
    result, steps = connected_components(body.graph)
    return {
        "success": True,
        "algorithm": "cc",
        "result": result,
        "visualization": {
            "steps": steps,
        },
    }


@router.post("/scc")
def scc_route(body: GraphAlgorithmRequest) -> dict[str, Any]:
    result = strongly_connected_components(body.graph)
    return {
        "success": True,
        "algorithm": "scc",
        "result": result,
    }


@router.post("/properties")
def graph_properties_route(body: GraphAlgorithmRequest) -> dict[str, Any]:
    analyzer = GraphAnalyzer(body.graph)
    return {
        "success": True,
        "algorithm": "graph-properties",
        "result": analyzer.analyze(),
    }
