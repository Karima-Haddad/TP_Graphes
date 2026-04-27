from __future__ import annotations

import colorsys
import time
from collections import defaultdict
from typing import Any

try:
    from backend.models.graph import GraphRequest
    from backend.utils.graph_utils import (
        GraphValidationError,
        build_adjacency_list,
        find_duplicate_edges,
        validate_graph,
    )
    from backend.utils.response_utils import make_response, make_step
except ModuleNotFoundError:  # pragma: no cover - compatibilite uvicorn depuis backend/
    from models.graph import GraphRequest
    from utils.graph_utils import (
        GraphValidationError,
        build_adjacency_list,
        find_duplicate_edges,
        validate_graph,
    )
    from utils.response_utils import make_response, make_step


PALETTE = [
    "#ef4444",
    "#3b82f6",
    "#22c55e",
    "#f59e0b",
    "#a855f7",
    "#14b8a6",
    "#ec4899",
    "#64748b",
]


def run_welsh_powell(graph: GraphRequest) -> dict[str, Any]:
    started_at = time.perf_counter()
    warnings: list[str] = []
    steps: list[dict[str, Any]] = []
    try:
        

        # Cas graphe vide
        if not graph.nodes:
            steps.append(
                make_step(
                    0,
                    "Graphe vide",
                    "Aucun sommet dans le graphe : 0 couleur.",
                    {
                        "highlighted_nodes": [],
                        "highlighted_edges": [],
                        "node_colors": {},
                        "edge_colors": {},
                        "node_labels": {},
                        "edge_labels": {},
                        "extra": {"color_count": 0},
                    },
                )
            )

            return make_response(
                success=True,
                algorithm="welsh_powell",
                message="Execution reussie",
                execution_time_ms=_elapsed_ms(started_at),
                result={
                    "summary": {"color_count": 0, "ordered_nodes": []},
                    "details": {"degrees": {}, "colors": {}, "color_groups": {}},
                },
                result_graph={
                    "highlighted_nodes": [],
                    "highlighted_edges": [],
                    "node_colors": {},
                    "edge_colors": {},
                    "node_labels": {},
                    "edge_labels": {},
                },
                steps=steps,
                warnings=warnings,
            )
        validate_graph(graph)

        self_loops = [edge.source for edge in graph.edges if edge.source == edge.target]
        if self_loops:
            raise GraphValidationError(
                "La coloration Welsh-Powell n'est pas definie pour un graphe avec boucle."
            )

        if graph.directed:
            warnings.append(
                "Welsh-Powell colore le graphe sous-jacent non oriente."
            )

        duplicates = find_duplicate_edges(graph, directed=False)
        if duplicates:
            warnings.append(
                "Des aretes en double ont ete ignorees pour calculer les degres."
            )

        adjacency = build_adjacency_list(graph, directed=False, as_sets=True)
        typed_adjacency = {node: set(neighbors) for node, neighbors in adjacency.items()}
        degrees = {node: len(typed_adjacency[node]) for node in graph.nodes}
        ordered_nodes = sorted(graph.nodes, key=lambda node: (-degrees[node], node))

        steps.append(
            make_step(
                len(steps),
                "Calcul des degres",
                "Le degre de chaque sommet est calcule a partir du graphe non oriente.",
                {
                    "node_labels": {node: f"d={degrees[node]}" for node in graph.nodes},
                    "extra": {"degrees": degrees},
                },
            )
        )
        steps.append(
            make_step(
                len(steps),
                "Tri des sommets",
                "Les sommets sont tries par degre decroissant avant la coloration.",
                {
                    "selected_nodes": ordered_nodes,
                    "node_labels": {
                        node: str(position + 1)
                        for position, node in enumerate(ordered_nodes)
                    },
                    "extra": {"ordered_nodes": ordered_nodes},
                },
            )
        )

        colors: dict[str, int] = {}
        color_index = 0

        while len(colors) < len(graph.nodes):
            color_index += 1
            color_nodes: list[str] = []

            for node in ordered_nodes:
                if node in colors:
                    continue

                conflicts = sorted(typed_adjacency[node].intersection(color_nodes))
                if conflicts:
                    steps.append(
                        make_step(
                            len(steps),
                            "Conflit de couleur",
                            (
                                f"Le sommet {node} ne peut pas recevoir la couleur C{color_index} "
                                f"car il est adjacent a {', '.join(conflicts)}."
                            ),
                            {
                                "highlighted_nodes": [node, *conflicts],
                                "selected_nodes": color_nodes,
                                "node_colors": _visual_node_colors(colors),
                                "extra": {
                                    "candidate": node,
                                    "color": color_index,
                                    "conflicts": conflicts,
                                },
                            },
                        )
                    )
                    continue

                colors[node] = color_index
                color_nodes.append(node)
                steps.append(
                    make_step(
                        len(steps),
                        "Coloration d'un sommet",
                        f"Le sommet {node} recoit la couleur C{color_index}.",
                        {
                            "highlighted_nodes": [node],
                            "visited_nodes": list(colors.keys()),
                            "selected_nodes": color_nodes,
                            "node_colors": _visual_node_colors(colors),
                            "node_labels": {
                                colored_node: f"C{color}"
                                for colored_node, color in colors.items()
                            },
                            "extra": {
                                "node": node,
                                "color": color_index,
                                "color_nodes": color_nodes.copy(),
                            },
                        },
                    )
                )

            steps.append(
                make_step(
                    len(steps),
                    "Couleur terminee",
                    f"La couleur C{color_index} est attribuee a {', '.join(color_nodes)}.",
                    {
                        "selected_nodes": color_nodes,
                        "node_colors": _visual_node_colors(colors),
                        "extra": {
                            "color": color_index,
                            "color_nodes": color_nodes.copy(),
                        },
                    },
                )
            )

        color_groups = _group_colors(colors)
        result_graph = {
            "highlighted_nodes": graph.nodes,
            "highlighted_edges": [],
            "node_colors": _visual_node_colors(colors),
            "edge_colors": {},
            "node_labels": {node: f"C{colors[node]}" for node in graph.nodes},
            "edge_labels": {},
        }
        result = {
            "summary": {
                "color_count": color_index,
                "ordered_nodes": ordered_nodes,
            },
            "details": {
                "degrees": degrees,
                "colors": colors,
                "color_groups": color_groups,
            },
        }

        return make_response(
            success=True,
            algorithm="welsh_powell",
            message="Execution reussie",
            execution_time_ms=_elapsed_ms(started_at),
            result=result,
            result_graph=result_graph,
            steps=steps,
            warnings=warnings,
        )

    except GraphValidationError as exc:
        return make_response(
            success=False,
            algorithm="welsh_powell",
            message="Erreur de validation du graphe",
            execution_time_ms=_elapsed_ms(started_at),
            warnings=warnings,
            error={"type": "GraphValidationError", "message": str(exc)},
        )


def _visual_node_colors(colors: dict[str, int]) -> dict[str, str]:
    return {node: _color_value(color) for node, color in colors.items()}


def _color_value(color_index: int) -> str:
    if color_index <= len(PALETTE):
        return PALETTE[color_index - 1]

    hue = ((color_index - 1) * 0.61803398875) % 1
    red, green, blue = colorsys.hsv_to_rgb(hue, 0.65, 0.88)
    return f"#{int(red * 255):02x}{int(green * 255):02x}{int(blue * 255):02x}"


def _group_colors(colors: dict[str, int]) -> dict[str, list[str]]:
    groups: dict[int, list[str]] = defaultdict(list)
    for node, color in colors.items():
        groups[color].append(node)
    return {f"C{color}": sorted(nodes) for color, nodes in sorted(groups.items())}


def _elapsed_ms(started_at: float) -> int:
    return round((time.perf_counter() - started_at) * 1000)
