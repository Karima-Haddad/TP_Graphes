from __future__ import annotations

from collections import deque
from typing import Iterable

try:
    from backend.models.graph import Edge, GraphRequest
except ModuleNotFoundError:  # pragma: no cover - compatibilite uvicorn depuis backend/
    from models.graph import Edge, GraphRequest


class GraphValidationError(ValueError):
    pass


def edge_id(edge: Edge, index: int, directed: bool) -> str:
    separator = "->" if directed else "--"
    return f"{edge.source}{separator}{edge.target}#{index}"


def validate_graph(graph: GraphRequest) -> None:
    if not graph.nodes:
        raise GraphValidationError("Le graphe est vide: ajoutez au moins un sommet.")

    if len(set(graph.nodes)) != len(graph.nodes):
        raise GraphValidationError("Le graphe contient des sommets en double.")

    node_set = set(graph.nodes)
    for index, edge in enumerate(graph.edges):
        missing = [node for node in (edge.source, edge.target) if node not in node_set]
        if missing:
            missing_text = ", ".join(missing)
            raise GraphValidationError(
                f"L'arete #{index} reference un sommet inexistant: {missing_text}."
            )


def build_adjacency_list(
    graph: GraphRequest,
    *,
    directed: bool | None = None,
    as_sets: bool = True,
) -> dict[str, set[str] | list[str]]:
    validate_graph(graph)
    is_directed = graph.directed if directed is None else directed
    adjacency: dict[str, set[str] | list[str]]

    if as_sets:
        adjacency = {node: set() for node in graph.nodes}
    else:
        adjacency = {node: [] for node in graph.nodes}

    for edge in graph.edges:
        _add_neighbor(adjacency, edge.source, edge.target, as_sets)
        if not is_directed:
            _add_neighbor(adjacency, edge.target, edge.source, as_sets)

    return adjacency


def _add_neighbor(
    adjacency: dict[str, set[str] | list[str]],
    source: str,
    target: str,
    as_sets: bool,
) -> None:
    if as_sets:
        casted = adjacency[source]
        assert isinstance(casted, set)
        casted.add(target)
        return

    casted = adjacency[source]
    assert isinstance(casted, list)
    casted.append(target)


def find_duplicate_edges(graph: GraphRequest, *, directed: bool | None = None) -> list[str]:
    is_directed = graph.directed if directed is None else directed
    seen: set[tuple[str, str]] = set()
    duplicates: list[str] = []

    for index, edge in enumerate(graph.edges):
        key = (edge.source, edge.target)
        if not is_directed and edge.source > edge.target:
            key = (edge.target, edge.source)

        if key in seen:
            duplicates.append(edge_id(edge, index, is_directed))
        else:
            seen.add(key)

    return duplicates


def incident_nodes(graph: GraphRequest) -> set[str]:
    nodes: set[str] = set()
    for edge in graph.edges:
        nodes.add(edge.source)
        nodes.add(edge.target)
    return nodes


def is_weakly_connected(graph: GraphRequest, active_nodes: Iterable[str] | None = None) -> bool:
    validate_graph(graph)
    active = set(active_nodes if active_nodes is not None else incident_nodes(graph))
    if not active:
        return True

    adjacency = build_adjacency_list(graph, directed=False, as_sets=True)
    start = next(iter(active))
    visited = _bfs(start, adjacency, active)
    return active.issubset(visited)


def connected_components(
    graph: GraphRequest,
    active_nodes: Iterable[str] | None = None,
) -> list[list[str]]:
    validate_graph(graph)
    active = set(active_nodes if active_nodes is not None else graph.nodes)
    adjacency = build_adjacency_list(graph, directed=False, as_sets=True)
    components: list[list[str]] = []
    visited: set[str] = set()

    for node in graph.nodes:
        if node not in active or node in visited:
            continue
        component = _bfs(node, adjacency, active)
        visited.update(component)
        components.append(sorted(component))

    return components


def _bfs(
    start: str,
    adjacency: dict[str, set[str] | list[str]],
    allowed_nodes: set[str],
) -> set[str]:
    queue: deque[str] = deque([start])
    visited = {start}

    while queue:
        node = queue.popleft()
        neighbors = adjacency[node]
        for neighbor in neighbors:
            if neighbor in allowed_nodes and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited
