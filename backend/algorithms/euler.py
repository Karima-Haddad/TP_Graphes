from __future__ import annotations

import time
from collections import defaultdict
from typing import Any

try:
    from backend.models.graph import Edge, GraphRequest
    from backend.utils.graph_utils import (
        GraphValidationError,
        connected_components,
        edge_id,
        incident_nodes,
        is_weakly_connected,
        validate_graph,
    )
    from backend.utils.response_utils import make_response, make_step
except ModuleNotFoundError:  # pragma: no cover - compatibilite uvicorn depuis backend/
    from models.graph import Edge, GraphRequest
    from utils.graph_utils import (
        GraphValidationError,
        connected_components,
        edge_id,
        incident_nodes,
        is_weakly_connected,
        validate_graph,
    )
    from utils.response_utils import make_response, make_step


def run_euler(graph: GraphRequest) -> dict[str, Any]:
    started_at = time.perf_counter()
    warnings: list[str] = []
    steps: list[dict[str, Any]] = []

    try:
        

        # Cas graphe vide
        if not graph.nodes:
            return make_response(
                success=True,
                algorithm="euler",
                message="Aucun cycle eulerien (graphe vide).",
                execution_time_ms=_elapsed_ms(started_at),
                result={
                    "summary": {"has_eulerian_cycle": False},
                    "details": {"cycle": []},
                },
                result_graph={
                    "highlighted_nodes": [],
                    "highlighted_edges": [],
                    "node_colors": {},
                    "edge_colors": {},
                    "node_labels": {},
                    "edge_labels": {},
                },
                steps=[
                    make_step(
                        0,
                        "Graphe vide",
                        "Le graphe est vide, donc aucun cycle eulerien.",
                        {},
                    )
                ],
                warnings=warnings,
            )
        validate_graph(graph)
        if graph.directed:
            classification = _classify_directed(graph, steps)
        else:
            classification = _classify_undirected(graph, steps)

        if not classification["connected"]:
            warnings.append("Le graphe n'est pas connexe sur ses sommets incidents.")
            result = _empty_euler_result(classification)
            steps.append(
                make_step(
                    len(steps),
                    "Graphe non connexe",
                    "Les aretes ne sont pas toutes dans la meme composante connexe.",
                    {
                        "extra": {
                            "components": classification["components"],
                            "reason": "not_connected",
                        }
                    },
                )
            )
            return make_response(
                success=True,
                algorithm="euler",
                message="Aucun chemin eulerien: le graphe n'est pas connexe.",
                execution_time_ms=_elapsed_ms(started_at),
                result=result,
                result_graph=_result_graph(graph, [], []),
                steps=steps,
                warnings=warnings,
            )

        if not classification["exists"]:
            result = _empty_euler_result(classification)
            steps.append(
                make_step(
                    len(steps),
                    "Condition eulerienne non satisfaite",
                    "Les degres du graphe ne permettent ni chemin ni circuit eulerien.",
                    {
                        "extra": {
                            "reason": classification["reason"],
                            "degree_data": classification["degree_data"],
                        }
                    },
                )
            )
            return make_response(
                success=True,
                algorithm="euler",
                message="Aucun chemin eulerien n'existe pour ce graphe.",
                execution_time_ms=_elapsed_ms(started_at),
                result=result,
                result_graph=_result_graph(graph, [], []),
                steps=steps,
                warnings=warnings,
            )

        if not graph.edges:
            start_node = graph.nodes[0]
            path = [start_node]
            steps.append(
                make_step(
                    len(steps),
                    "Circuit trivial",
                    "Le graphe ne contient aucune arete: un sommet seul forme un circuit trivial.",
                    {
                        "highlighted_nodes": [start_node],
                        "extra": {"path": path},
                    },
                )
            )
            result = _euler_result(classification, path, [])
            return make_response(
                success=True,
                algorithm="euler",
                message="Execution reussie",
                execution_time_ms=_elapsed_ms(started_at),
                result=result,
                result_graph=_result_graph(graph, path, []),
                steps=steps,
                warnings=warnings,
            )

        path, path_edge_ids = _hierholzer(graph, classification["start"], steps)

        if len(path_edge_ids) != len(graph.edges):
            warnings.append(
                "Hierholzer n'a pas consomme toutes les aretes; le graphe est probablement deconnecte."
            )
            classification["exists"] = False
            classification["type"] = "aucun"
            classification["reason"] = "unused_edges"
            result = _empty_euler_result(classification)
            return make_response(
                success=True,
                algorithm="euler",
                message="Aucun chemin eulerien n'a pu etre construit.",
                execution_time_ms=_elapsed_ms(started_at),
                result=result,
                result_graph=_result_graph(graph, [], []),
                steps=steps,
                warnings=warnings,
            )

        steps.append(
            make_step(
                len(steps),
                "Chemin construit",
                "Le chemin obtenu utilise chaque arete exactement une fois.",
                {
                    "highlighted_nodes": path,
                    "highlighted_edges": path_edge_ids,
                    "selected_nodes": path,
                    "selected_edges": path_edge_ids,
                    "extra": {"path": path, "type": classification["type"]},
                },
            )
        )

        result = _euler_result(classification, path, path_edge_ids)
        return make_response(
            success=True,
            algorithm="euler",
            message="Execution reussie",
            execution_time_ms=_elapsed_ms(started_at),
            result=result,
            result_graph=_result_graph(graph, path, path_edge_ids),
            steps=steps,
            warnings=warnings,
        )

    except GraphValidationError as exc:
        return make_response(
            success=False,
            algorithm="euler",
            message="Erreur de validation du graphe",
            execution_time_ms=_elapsed_ms(started_at),
            warnings=warnings,
            error={"type": "GraphValidationError", "message": str(exc)},
        )


def _classify_undirected(
    graph: GraphRequest,
    steps: list[dict[str, Any]],
) -> dict[str, Any]:
    degrees = {node: 0 for node in graph.nodes}
    for edge in graph.edges:
        if edge.source == edge.target:
            degrees[edge.source] += 2
        else:
            degrees[edge.source] += 1
            degrees[edge.target] += 1

    active_nodes = {node for node, degree in degrees.items() if degree > 0}
    components = connected_components(graph, active_nodes or graph.nodes)
    connected = is_weakly_connected(graph, active_nodes)
    odd_nodes = sorted(node for node, degree in degrees.items() if degree % 2 == 1)

    steps.append(
        make_step(
            len(steps),
            "Analyse des degres",
            "Pour un graphe non oriente, on compte les sommets de degre impair.",
            {
                "node_labels": {node: f"d={degree}" for node, degree in degrees.items()},
                "extra": {
                    "degrees": degrees,
                    "odd_nodes": odd_nodes,
                    "active_nodes": sorted(active_nodes),
                },
            },
        )
    )
    steps.append(
        make_step(
            len(steps),
            "Verification de connexite",
            "Les sommets incidents doivent appartenir a une seule composante connexe.",
            {
                "selected_nodes": sorted(active_nodes),
                "extra": {"connected": connected, "components": components},
            },
        )
    )

    if not graph.edges:
        euler_type = "circuit_eulerien"
        exists = True
        start = graph.nodes[0]
        reason = "trivial_empty_edges"
    elif len(odd_nodes) == 0:
        euler_type = "circuit_eulerien"
        exists = True
        start = _first_active_node(graph, active_nodes)
        reason = "all_degrees_even"
    elif len(odd_nodes) == 2:
        euler_type = "chemin_eulerien"
        exists = True
        start = odd_nodes[0]
        reason = "two_odd_vertices"
    else:
        euler_type = "aucun"
        exists = False
        start = None
        reason = "invalid_odd_vertex_count"

    steps.append(
        make_step(
            len(steps),
            "Test eulerien",
            _condition_description(euler_type, graph.directed, reason),
            {
                "selected_nodes": odd_nodes,
                "extra": {
                    "exists": exists and connected,
                    "type": euler_type if exists and connected else "aucun",
                    "reason": reason,
                    "start": start,
                },
            },
        )
    )

    return {
        "exists": exists and connected,
        "type": euler_type if exists and connected else "aucun",
        "start": start,
        "connected": connected,
        "components": components,
        "reason": reason,
        "degree_data": {"degrees": degrees, "odd_nodes": odd_nodes},
    }


def _classify_directed(
    graph: GraphRequest,
    steps: list[dict[str, Any]],
) -> dict[str, Any]:
    in_degrees = {node: 0 for node in graph.nodes}
    out_degrees = {node: 0 for node in graph.nodes}

    for edge in graph.edges:
        out_degrees[edge.source] += 1
        in_degrees[edge.target] += 1

    active_nodes = incident_nodes(graph)
    components = connected_components(graph, active_nodes or graph.nodes)
    connected = is_weakly_connected(graph, active_nodes)
    start_candidates: list[str] = []
    end_candidates: list[str] = []
    invalid_nodes: list[str] = []

    for node in graph.nodes:
        diff = out_degrees[node] - in_degrees[node]
        if diff == 1:
            start_candidates.append(node)
        elif diff == -1:
            end_candidates.append(node)
        elif diff != 0:
            invalid_nodes.append(node)

    steps.append(
        make_step(
            len(steps),
            "Analyse des degres",
            "Pour un graphe oriente, on compare degre sortant et degre entrant.",
            {
                "node_labels": {
                    node: f"+{out_degrees[node]}/-{in_degrees[node]}"
                    for node in graph.nodes
                },
                "extra": {
                    "in_degrees": in_degrees,
                    "out_degrees": out_degrees,
                    "start_candidates": start_candidates,
                    "end_candidates": end_candidates,
                    "invalid_nodes": invalid_nodes,
                    "active_nodes": sorted(active_nodes),
                },
            },
        )
    )
    steps.append(
        make_step(
            len(steps),
            "Verification de connexite faible",
            "Les sommets incidents doivent etre connectes si on ignore le sens des arcs.",
            {
                "selected_nodes": sorted(active_nodes),
                "extra": {"connected": connected, "components": components},
            },
        )
    )

    if not graph.edges:
        euler_type = "circuit_eulerien"
        exists = True
        start = graph.nodes[0]
        reason = "trivial_empty_edges"
    elif not start_candidates and not end_candidates and not invalid_nodes:
        euler_type = "circuit_eulerien"
        exists = True
        start = _first_active_node(graph, active_nodes)
        reason = "balanced_degrees"
    elif (
        len(start_candidates) == 1
        and len(end_candidates) == 1
        and not invalid_nodes
    ):
        euler_type = "chemin_eulerien"
        exists = True
        start = start_candidates[0]
        reason = "one_start_one_end"
    else:
        euler_type = "aucun"
        exists = False
        start = None
        reason = "invalid_directed_degree_balance"

    steps.append(
        make_step(
            len(steps),
            "Test eulerien",
            _condition_description(euler_type, graph.directed, reason),
            {
                "selected_nodes": [node for node in [start, *end_candidates] if node],
                "extra": {
                    "exists": exists and connected,
                    "type": euler_type if exists and connected else "aucun",
                    "reason": reason,
                    "start": start,
                },
            },
        )
    )

    return {
        "exists": exists and connected,
        "type": euler_type if exists and connected else "aucun",
        "start": start,
        "connected": connected,
        "components": components,
        "reason": reason,
        "degree_data": {
            "in_degrees": in_degrees,
            "out_degrees": out_degrees,
            "start_candidates": start_candidates,
            "end_candidates": end_candidates,
            "invalid_nodes": invalid_nodes,
        },
    }


def _hierholzer(
    graph: GraphRequest,
    start: str,
    steps: list[dict[str, Any]],
) -> tuple[list[str], list[str]]:
    adjacency = _edge_adjacency(graph)
    used_edges: set[str] = set()
    stack: list[tuple[str, str | None]] = [(start, None)]
    circuit_nodes: list[str] = []
    circuit_edges: list[str] = []

    steps.append(
        make_step(
            len(steps),
            "Initialisation de Hierholzer",
            f"L'algorithme demarre au sommet {start}.",
            {
                "highlighted_nodes": [start],
                "extra": {"stack": [start], "used_edges": []},
            },
        )
    )

    while stack:
        current_node = stack[-1][0]

        while adjacency[current_node] and adjacency[current_node][-1][1] in used_edges:
            adjacency[current_node].pop()

        if adjacency[current_node]:
            next_node, current_edge_id = adjacency[current_node].pop()
            used_edges.add(current_edge_id)
            stack.append((next_node, current_edge_id))
            steps.append(
                make_step(
                    len(steps),
                    "Parcours d'une arete",
                    f"L'arete {current_edge_id} est ajoutee au parcours.",
                    {
                        "highlighted_nodes": [current_node, next_node],
                        "highlighted_edges": [current_edge_id],
                        "selected_nodes": [node for node, _ in stack],
                        "selected_edges": list(used_edges),
                        "extra": {
                            "from": current_node,
                            "to": next_node,
                            "edge": current_edge_id,
                            "stack": [node for node, _ in stack],
                        },
                    },
                )
            )
        else:
            popped_node, incoming_edge = stack.pop()
            circuit_nodes.append(popped_node)
            if incoming_edge is not None:
                circuit_edges.append(incoming_edge)
            steps.append(
                make_step(
                    len(steps),
                    "Retour arriere",
                    f"Le sommet {popped_node} est ajoute au chemin final partiel.",
                    {
                        "highlighted_nodes": [popped_node],
                        "selected_nodes": [node for node, _ in stack],
                        "extra": {
                            "partial_path_reversed": circuit_nodes.copy(),
                            "stack": [node for node, _ in stack],
                        },
                    },
                )
            )

    circuit_nodes.reverse()
    circuit_edges.reverse()
    return circuit_nodes, circuit_edges


def _edge_adjacency(graph: GraphRequest) -> dict[str, list[tuple[str, str]]]:
    adjacency: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for node in graph.nodes:
        adjacency[node] = []

    indexed_edges = list(enumerate(graph.edges))
    for index, edge in reversed(indexed_edges):
        current_edge_id = edge_id(edge, index, graph.directed)
        adjacency[edge.source].append((edge.target, current_edge_id))
        if not graph.directed and edge.source != edge.target:
            adjacency[edge.target].append((edge.source, current_edge_id))
        elif not graph.directed and edge.source == edge.target:
            adjacency[edge.target].append((edge.source, current_edge_id))

    return adjacency


def _first_active_node(graph: GraphRequest, active_nodes: set[str]) -> str:
    for node in graph.nodes:
        if node in active_nodes:
            return node
    return graph.nodes[0]


def _condition_description(euler_type: str, directed: bool, reason: str) -> str:
    if euler_type == "circuit_eulerien":
        if directed:
            return "Tous les sommets ont autant d'arcs entrants que sortants."
        return "Tous les sommets ont un degre pair."
    if euler_type == "chemin_eulerien":
        if directed:
            return "Un sommet peut demarrer le chemin et un autre peut le terminer."
        return "Exactement deux sommets ont un degre impair."
    return f"Les conditions euleriennes ne sont pas satisfaites ({reason})."


def _empty_euler_result(classification: dict[str, Any]) -> dict[str, Any]:
    return {
        "summary": {
            "exists": False,
            "type": "aucun",
            "path": [],
        },
        "details": {
            "reason": classification["reason"],
            "connected": classification["connected"],
            "components": classification["components"],
            "degree_data": classification["degree_data"],
        },
    }


def _euler_result(
    classification: dict[str, Any],
    path: list[str],
    path_edge_ids: list[str],
) -> dict[str, Any]:
    return {
        "summary": {
            "exists": True,
            "type": classification["type"],
            "path": path,
        },
        "details": {
            "start": classification["start"],
            "edge_path": path_edge_ids,
            "connected": classification["connected"],
            "components": classification["components"],
            "degree_data": classification["degree_data"],
        },
    }


def _result_graph(
    graph: GraphRequest,
    path: list[str],
    path_edge_ids: list[str],
) -> dict[str, Any]:
    return {
        "highlighted_nodes": path,
        "highlighted_edges": path_edge_ids,
        "node_colors": {node: "#22c55e" for node in path},
        "edge_colors": {edge: "#f97316" for edge in path_edge_ids},
        "node_labels": {node: node for node in graph.nodes},
        "edge_labels": {
            edge_id(edge, index, graph.directed): str(index + 1)
            for index, edge in enumerate(graph.edges)
        },
    }


def _elapsed_ms(started_at: float) -> int:
    return round((time.perf_counter() - started_at) * 1000)
