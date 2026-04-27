"""
shortest_path_routes.py — Routes FastAPI pour les algorithmes de plus court chemin.

Expose un seul endpoint POST /api/shortest-path qui dispatch
vers Dijkstra, Bellman-Ford ou Bellman selon le champ "algorithm".
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Any, Optional

from services.shortest_path_service import run_shortest_path

router = APIRouter(prefix="/api/shortest-path", tags=["Shortest Path"])


# ─────────────────────────────────────────────
# Schémas de validation de la requête (Pydantic)
# ─────────────────────────────────────────────

class NodeModel(BaseModel):
    id: str
    label: Optional[str] = None
    x: Optional[float] = 0.0
    y: Optional[float] = 0.0
    data: Optional[dict] = {}


class EdgeModel(BaseModel):
    id: str
    source: str
    target: str
    weight: Optional[float] = 1.0
    label: Optional[str] = ""
    data: Optional[dict] = {}


class GraphModel(BaseModel):
    directed: bool
    weighted: bool
    nodes: list[NodeModel]
    edges: list[EdgeModel]


class ShortestPathParams(BaseModel):
    source: str = Field(..., description="Identifiant du nœud source")
    target: str = Field(..., description="Identifiant du nœud cible")


class ShortestPathRequest(BaseModel):
    algorithm: str = Field(
        ...,
        description="Algorithme à utiliser : 'dijkstra', 'bellman-ford' ou 'bellman'"
    )
    graph: GraphModel
    params: ShortestPathParams


# ─────────────────────────────────────────────
# Endpoint principal
# ─────────────────────────────────────────────

@router.post("/run")
def run_shortest_path_endpoint(request: ShortestPathRequest) -> dict[str, Any]:
    """
    Exécute un algorithme de plus court chemin sur le graphe fourni.

    - **dijkstra**    : graphe pondéré à poids positifs uniquement
    - **bellman-ford** : graphe pondéré, poids négatifs autorisés, détecte les cycles négatifs
    - **bellman**     : graphe orienté acyclique (DAG), version simplifiée du cours
    """
    # Conversion du modèle Pydantic en dict brut pour les algorithmes
    graph_data = request.graph.model_dump()
    params = request.params.model_dump()

    return run_shortest_path(request.algorithm, graph_data, params)