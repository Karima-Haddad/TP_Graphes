from __future__ import annotations

from typing import Any


def empty_graph_state() -> dict[str, Any]:
    return {
        "highlighted_nodes": [],
        "highlighted_edges": [],
        "visited_nodes": [],
        "selected_nodes": [],
        "selected_edges": [],
        "node_labels": {},
        "edge_labels": {},
        "node_colors": {},
        "edge_colors": {},
        "extra": {},
    }


def empty_result_graph() -> dict[str, Any]:
    return {
        "highlighted_nodes": [],
        "highlighted_edges": [],
        "node_colors": {},
        "edge_colors": {},
        "node_labels": {},
        "edge_labels": {},
    }


def make_step(
    index: int,
    title: str,
    description: str,
    state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    step_state = empty_graph_state()
    if state:
        step_state.update(state)
    return {
        "index": index,
        "title": title,
        "description": description,
        "state": step_state,
    }


def make_response(
    *,
    success: bool,
    algorithm: str,
    message: str,
    execution_time_ms: int,
    params: dict[str, Any] | None = None,
    result: dict[str, Any] | None = None,
    result_graph: dict[str, Any] | None = None,
    steps: list[dict[str, Any]] | None = None,
    warnings: list[str] | None = None,
    error: dict[str, Any] | None = None,
) -> dict[str, Any]:
    steps = steps or []
    return {
        "success": success,
        "algorithm": algorithm,
        "message": message,
        "params": params or {},
        "result": result or {"summary": {}, "details": {}},
        "visualization": {
            "result_graph": result_graph or empty_result_graph(),
            "steps": steps,
        },
        "meta": {
            "execution_time_ms": execution_time_ms,
            "step_count": len(steps),
            "warnings": warnings or [],
        },
        "error": error,
    }
