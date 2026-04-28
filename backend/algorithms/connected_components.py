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


def connected_components(graph):
    nodes = [get_node_id(n) for n in graph["nodes"]]
    edges = graph["edges"]

    adj = {n: [] for n in nodes}

    for e in edges:
        u, v = e["source"], e["target"]
        edge_id = get_edge_id(e)

        adj[u].append((v, edge_id))
        adj[v].append((u, edge_id))

    visited = set()
    components = []
    steps = []

    def add_step(title, description, highlighted_nodes=None,
                 highlighted_edges=None, selected_nodes=None,
                 selected_edges=None, extra=None):
        steps.append({
            "title": title,
            "description": description,
            "state": {
                "visited_nodes": list(visited),
                "selected_nodes": selected_nodes or [],
                "selected_edges": selected_edges or [],
                "highlighted_nodes": highlighted_nodes or [],
                "highlighted_edges": highlighted_edges or [],
                "node_labels": {},
                "edge_labels": {},
                "extra": extra or {}
            }
        })

    def dfs(node, comp, comp_edges):
        visited.add(node)
        comp.append(node)

        add_step(
            title=f"Visite du sommet {node}",
            description=(
                f"Le sommet {node} est marqué comme visité. "
                f"Il est ajouté à la composante courante."
            ),
            highlighted_nodes=[node],
            selected_nodes=list(comp),
            selected_edges=list(comp_edges),
            extra={
                "phase": "DFS",
                "current_node": node,
                "component": list(comp)
            }
        )

        for neigh, edge_id in adj[node]:
            add_step(
                title=f"Examen de l’arête {node} — {neigh}",
                description=(
                    f"L’algorithme vérifie si le voisin {neigh} "
                    f"a déjà été visité."
                ),
                highlighted_nodes=[node, neigh],
                highlighted_edges=[edge_id],
                selected_nodes=list(comp),
                selected_edges=list(comp_edges),
                extra={
                    "phase": "DFS",
                    "current_node": node,
                    "neighbor": neigh
                }
            )

            if neigh not in visited:
                comp_edges.append(edge_id)

                add_step(
                    title=f"Exploration vers {neigh}",
                    description=(
                        f"Le sommet {neigh} n’est pas encore visité. "
                        f"DFS poursuit donc l’exploration depuis {node} vers {neigh}."
                    ),
                    highlighted_nodes=[node, neigh],
                    highlighted_edges=[edge_id],
                    selected_nodes=list(comp),
                    selected_edges=list(comp_edges),
                    extra={
                        "phase": "DFS",
                        "current_node": node,
                        "next_node": neigh
                    }
                )

                dfs(neigh, comp, comp_edges)

            else:
                add_step(
                    title=f"{neigh} déjà visité",
                    description=(
                        f"Le sommet {neigh} appartient déjà à une composante "
                        f"en cours ou terminée. On ne le revisite pas."
                    ),
                    highlighted_nodes=[node, neigh],
                    highlighted_edges=[edge_id],
                    selected_nodes=list(comp),
                    selected_edges=list(comp_edges),
                    extra={
                        "phase": "DFS",
                        "current_node": node,
                        "already_visited": neigh
                    }
                )

    for node in nodes:
        if node not in visited:
            comp = []
            comp_edges = []

            add_step(
                title="Début d’une nouvelle composante",
                description=(
                    f"Le sommet {node} n’a pas encore été visité. "
                    f"On démarre une nouvelle recherche DFS à partir de ce sommet."
                ),
                highlighted_nodes=[node],
                selected_nodes=[],
                selected_edges=[],
                extra={
                    "phase": "new_component",
                    "start_node": node
                }
            )

            dfs(node, comp, comp_edges)

            components.append(comp)

            add_step(
                title="Composante terminée",
                description=(
                    f"Tous les sommets accessibles depuis {node} ont été explorés. "
                    f"La composante trouvée est : {' → '.join(comp)}."
                ),
                highlighted_nodes=list(comp),
                highlighted_edges=list(comp_edges),
                selected_nodes=list(comp),
                selected_edges=list(comp_edges),
                extra={
                    "phase": "component_finished",
                    "component": list(comp)
                }
            )

    return {
        "summary": {
            "count": len(components)
        },
        "details": {
            "components": components
        }
    }, steps


def run_connected_components(graph: GraphRequest) -> dict[str, Any]:
    started_at = time.perf_counter()

    try:
        result, steps = connected_components(graph.model_dump())

        return make_response(
            success=True,
            algorithm="connected_components",
            message=f"Trouvé {result['summary']['count']} composante(s) connexe(s)",
            execution_time_ms=(time.perf_counter() - started_at) * 1000,
            result=result,
            steps=steps
        )

    except Exception as e:
        return make_response(
            success=False,
            algorithm="connected_components",
            message=f"Erreur: {str(e)}",
            execution_time_ms=(time.perf_counter() - started_at) * 1000,
            error=str(e)
        )