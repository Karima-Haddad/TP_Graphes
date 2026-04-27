"""
Modèles Pydantic — Graphe et résultats ACM (Prim / Kruskal)
"""

from __future__ import annotations
from typing import Any
from pydantic import BaseModel, field_validator, model_validator


# ──────────────────────────────────────────────────────────────────────────────
#  Structures du graphe d'entrée
# ──────────────────────────────────────────────────────────────────────────────

class NodeModel(BaseModel):
    id: str
    label: str | None = None
    x: float | None = None
    y: float | None = None
    data: dict[str, Any] = {}


class EdgeModel(BaseModel):
    id: str
    source: str
    target: str
    weight: float | None = None
    label: str | None = None
    data: dict[str, Any] = {}


class GraphModel(BaseModel):
    directed: bool = False
    weighted: bool = True
    nodes: list[NodeModel]
    edges: list[EdgeModel]

    @field_validator("nodes")
    @classmethod
    def nodes_not_empty(cls, v: list[NodeModel]) -> list[NodeModel]:
        if not v:
            raise ValueError("Le graphe doit contenir au moins un sommet.")
        return v

    @model_validator(mode="after")
    def edges_reference_existing_nodes(self) -> "GraphModel":
        node_ids = {n.id for n in self.nodes}
        for e in self.edges:
            if e.source not in node_ids:
                raise ValueError(
                    f"L'arête '{e.id}' référence un sommet source inexistant : '{e.source}'."
                )
            if e.target not in node_ids:
                raise ValueError(
                    f"L'arête '{e.id}' référence un sommet cible inexistant : '{e.target}'."
                )
        return self


# ──────────────────────────────────────────────────────────────────────────────
#  Requêtes d'exécution
# ──────────────────────────────────────────────────────────────────────────────

class PrimParams(BaseModel):
    """Paramètres propres à Prim."""
    start_node: str | None = None


class KruskalParams(BaseModel):
    """Kruskal ne nécessite pas de paramètre."""
    pass


class MSTRequest(BaseModel):
    """Corps de requête commun pour Prim et Kruskal."""
    algorithm: str       # "prim" | "kruskal"
    graph: GraphModel
    params: dict[str, Any] = {}


# ──────────────────────────────────────────────────────────────────────────────
#  Structures de réponse
# ──────────────────────────────────────────────────────────────────────────────

class MSTEdgeInfo(BaseModel):
    id: str
    source: str
    target: str
    weight: float


class MSTResultSummary(BaseModel):
    total_cost: float


class MSTResultDetails(BaseModel):
    mst_edges: list[str]
    mst_nodes: list[str]
    edge_list: list[MSTEdgeInfo]


class MSTResult(BaseModel):
    summary: MSTResultSummary
    details: MSTResultDetails


class StepState(BaseModel):
    highlighted_nodes: list[str] = []
    highlighted_edges: list[str] = []
    visited_nodes: list[str] = []
    selected_nodes: list[str] = []
    selected_edges: list[str] = []
    node_labels: dict[str, str] = {}
    edge_labels: dict[str, str] = {}
    node_colors: dict[str, str] = {}
    edge_colors: dict[str, str] = {}
    extra: dict[str, Any] = {}


class Step(BaseModel):
    index: int
    title: str
    description: str
    state: StepState


class ResultGraph(BaseModel):
    highlighted_nodes: list[str] = []
    highlighted_edges: list[str] = []
    node_colors: dict[str, str] = {}
    edge_colors: dict[str, str] = {}
    node_labels: dict[str, str] = {}
    edge_labels: dict[str, str] = {}


class Visualization(BaseModel):
    result_graph: ResultGraph
    steps: list[Step]


class Meta(BaseModel):
    execution_time_ms: float
    step_count: int
    warnings: list[str]


class ErrorDetail(BaseModel):
    code: str
    type: str
    field: str | None = None
    details: dict[str, Any] = {}


class MSTResponse(BaseModel):
    success: bool
    algorithm: str
    message: str
    params: dict[str, Any]
    result: MSTResult | None
    visualization: Visualization | None
    meta: Meta
    error: ErrorDetail | None