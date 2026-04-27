from backend.algorithms.welsh_powell import run_welsh_powell
from backend.models.graph import Edge, GraphRequest


def make_graph(nodes, edges, directed=False):
    return GraphRequest(
        nodes=nodes,
        edges=[Edge(source=source, target=target) for source, target in edges],
        directed=directed,
    )


def test_welsh_powell_simple_graph():
    graph = make_graph(
        ["A", "B", "C", "D"],
        [("A", "B"), ("A", "C"), ("B", "D")],
    )

    response = run_welsh_powell(graph)

    assert response["success"] is True
    assert response["result"]["summary"]["color_count"] == 2
    assert set(response["result"]["details"]["colors"]) == {"A", "B", "C", "D"}
    assert response["meta"]["step_count"] == len(response["visualization"]["steps"])


def test_welsh_powell_even_cycle():
    graph = make_graph(
        ["A", "B", "C", "D"],
        [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")],
    )

    response = run_welsh_powell(graph)

    assert response["success"] is True
    assert response["result"]["summary"]["color_count"] == 2


def test_welsh_powell_odd_cycle():
    graph = make_graph(
        ["A", "B", "C", "D", "E"],
        [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A")],
    )

    response = run_welsh_powell(graph)

    assert response["success"] is True
    assert response["result"]["summary"]["color_count"] == 3


def test_welsh_powell_complete_graph():
    graph = make_graph(
        ["A", "B", "C", "D"],
        [
            ("A", "B"),
            ("A", "C"),
            ("A", "D"),
            ("B", "C"),
            ("B", "D"),
            ("C", "D"),
        ],
    )

    response = run_welsh_powell(graph)

    assert response["success"] is True
    assert response["result"]["summary"]["color_count"] == 4


def test_welsh_powell_graph_without_edges():
    graph = make_graph(["A", "B", "C"], [])

    response = run_welsh_powell(graph)

    assert response["success"] is True
    assert response["result"]["summary"]["color_count"] == 1
    assert set(response["result"]["details"]["color_groups"]["C1"]) == {"A", "B", "C"}
