from backend.algorithms.euler import run_euler
from backend.models.graph import Edge, GraphRequest


def make_graph(nodes, edges, directed=False):
    return GraphRequest(
        nodes=nodes,
        edges=[Edge(source=source, target=target) for source, target in edges],
        directed=directed,
    )


def test_euler_undirected_circuit():
    graph = make_graph(
        ["A", "B", "C"],
        [("A", "B"), ("B", "C"), ("C", "A")],
    )

    response = run_euler(graph)
    summary = response["result"]["summary"]

    assert response["success"] is True
    assert summary["exists"] is True
    assert summary["type"] == "circuit_eulerien"
    assert summary["path"][0] == summary["path"][-1]
    assert len(summary["path"]) == len(graph.edges) + 1


def test_euler_undirected_path():
    graph = make_graph(
        ["A", "B", "C"],
        [("A", "B"), ("B", "C")],
    )

    response = run_euler(graph)
    summary = response["result"]["summary"]

    assert response["success"] is True
    assert summary["exists"] is True
    assert summary["type"] == "chemin_eulerien"
    assert summary["path"][0] in {"A", "C"}
    assert summary["path"][-1] in {"A", "C"}
    assert summary["path"][0] != summary["path"][-1]


def test_euler_without_eulerian_path():
    graph = make_graph(
        ["A", "B", "C", "D"],
        [("A", "B"), ("A", "C"), ("A", "D")],
    )

    response = run_euler(graph)
    summary = response["result"]["summary"]

    assert response["success"] is True
    assert summary["exists"] is False
    assert summary["type"] == "aucun"
    assert summary["path"] == []


def test_euler_disconnected_graph():
    graph = make_graph(
        ["A", "B", "C", "D"],
        [("A", "B"), ("C", "D")],
    )

    response = run_euler(graph)
    summary = response["result"]["summary"]

    assert response["success"] is True
    assert summary["exists"] is False
    assert summary["type"] == "aucun"
    assert "connexe" in response["message"]


def test_euler_directed_path():
    graph = make_graph(
        ["A", "B", "C"],
        [("A", "B"), ("B", "C")],
        directed=True,
    )

    response = run_euler(graph)
    summary = response["result"]["summary"]

    assert response["success"] is True
    assert summary["exists"] is True
    assert summary["type"] == "chemin_eulerien"
    assert summary["path"] == ["A", "B", "C"]
