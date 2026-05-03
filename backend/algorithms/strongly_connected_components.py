from __future__ import annotations
import time
from typing import Any

try:
    from backend.models.graph import GraphRequest
    from backend.utils.response_utils import make_response
except ModuleNotFoundError:
    from models.graph import GraphRequest
    from utils.response_utils import make_response


def get_node_id(node):
    return node["id"] if isinstance(node, dict) else node


def get_edge_id(edge):
    return edge.get("id") or f"{edge['source']}-{edge['target']}"


# =========================================================
# 🔥 STRONGLY CONNECTED COMPONENTS (KOSARAJU)
# =========================================================
def strongly_connected_components(graph):
    nodes = [get_node_id(n) for n in graph["nodes"]]
    edges = graph["edges"]

    # ⚠️ check directed graph
    if not graph.get("directed", False):
        raise ValueError("Cet algorithme (CFC) nécessite un graphe orienté")

    # adjacency lists
    adj = {n: [] for n in nodes}
    rev = {n: [] for n in nodes}

    for e in edges:
        u = e.get("source")
        v = e.get("target")

        if u is None or v is None:
            continue

        edge_id = get_edge_id(e)

        adj[u].append((v, edge_id))
        rev[v].append((u, edge_id))

    visited = set()
    stack = []
    steps = []

    # =====================================================
    def add_step(title, description,
                 highlighted_nodes=None,
                 highlighted_edges=None,
                 selected_nodes=None,
                 selected_edges=None,
                 extra=None):

        steps.append({
            "title": title,
            "description": description,
            "state": {
                "visited_nodes": list(visited),
                "selected_nodes": selected_nodes or [],
                "selected_edges": selected_edges or [],
                "highlighted_nodes": highlighted_nodes or [],
                "highlighted_edges": highlighted_edges or [],
                "extra": extra or {}
            }
        })

    # =====================================================
    # 🔵 PHASE 1 : DFS + STACK
    def dfs1(node):
        visited.add(node)

        add_step(
            title=f"Phase 1 — Visite {node}",
            description=f"On explore {node} pour calculer l'ordre de fin.",
            highlighted_nodes=[node],
            extra={"phase": 1}
        )

        for neigh, edge_id in adj[node]:
            add_step(
                title=f"Arc {node} → {neigh}",
                description="Exploration des voisins",
                highlighted_nodes=[node, neigh],
                highlighted_edges=[edge_id],
                extra={"phase": 1}
            )

            if neigh not in visited:
                dfs1(neigh)

        stack.append(node)

        add_step(
            title=f"Empilement {node}",
            description="Ajout dans la pile selon l'ordre de fin",
            highlighted_nodes=[node],
            selected_nodes=list(stack),
            extra={"phase": 1, "stack": list(stack)}
        )

    # lancement phase 1
    for node in nodes:
        if node not in visited:
            dfs1(node)

    # =====================================================
    # 🔴 PHASE 2 : TRANSPOSE + DFS
    visited.clear()
    components = []

    add_step(
        title="Phase 2 — Graphe transposé",
        description="On inverse les arcs pour détecter les CFC",
        extra={"phase": 2}
    )

    def dfs2(node, comp, comp_edges):
        visited.add(node)
        comp.append(node)

        for neigh, edge_id in rev[node]:
            if neigh not in visited:
                comp_edges.append(edge_id)
                dfs2(neigh, comp, comp_edges)

    while stack:
        node = stack.pop()

        if node not in visited:
            comp = []
            comp_edges = []

            dfs2(node, comp, comp_edges)
            components.append(comp)

            add_step(
                title="CFC trouvée",
                description=f"Composante : {' → '.join(comp)}",
                highlighted_nodes=comp,
                highlighted_edges=comp_edges,
                selected_nodes=comp,
                selected_edges=comp_edges,
                extra={"component": comp}
            )

    return {
        "summary": {
            "count": len(components)
        },
        "details": {
            "components": components
        }
    }, steps


# =========================================================
# 🚀 API ENTRY POINT
# =========================================================
def run_strongly_connected_components(graph: GraphRequest) -> dict[str, Any]:
    started_at = time.perf_counter()

    try:
        result, steps = strongly_connected_components(graph.model_dump())

        return make_response(
            success=True,
            algorithm="strongly_connected_components",
            message=f"{result['summary']['count']} CFC trouvées",
            execution_time_ms=(time.perf_counter() - started_at) * 1000,
            result=result,
            steps=steps
        )

    except Exception as e:
        return make_response(
            success=False,
            algorithm="strongly_connected_components",
            message=str(e),
            execution_time_ms=(time.perf_counter() - started_at) * 1000,
            error=str(e)
        )
