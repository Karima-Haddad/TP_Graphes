"""
Tests unitaires — Prim & Kruskal
Couvre : cas normaux, graphes non connexes, arêtes manquantes, paramètres invalides.
Run : python -m pytest backend/tests/test_mst.py -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.algorithms.kruskal import run_kruskal
from backend.algorithms.prim import run_prim


# ──────────────────────────────────────────────────────────────────────────────
#  Graphe de référence (5 sommets, graphe du contrat)
# ──────────────────────────────────────────────────────────────────────────────

GRAPH_5 = {
    "directed": False,
    "weighted": True,
    "nodes": [
        {"id": "A", "label": "A", "x": 120, "y": 80},
        {"id": "B", "label": "B", "x": 290, "y": 130},
        {"id": "C", "label": "C", "x": 110, "y": 210},
        {"id": "D", "label": "D", "x": 320, "y": 240},
        {"id": "E", "label": "E", "x": 430, "y": 190},
    ],
    "edges": [
        {"id": "e1", "source": "A", "target": "B", "weight": 4},
        {"id": "e2", "source": "A", "target": "C", "weight": 2},
        {"id": "e3", "source": "B", "target": "D", "weight": 5},
        {"id": "e4", "source": "C", "target": "D", "weight": 1},
        {"id": "e5", "source": "D", "target": "E", "weight": 3},
    ],
}

# ──────────────────────────────────────────────────────────────────────────────
#  Kruskal — cas normaux
# ──────────────────────────────────────────────────────────────────────────────

def test_kruskal_basic():
    res = run_kruskal(GRAPH_5, {})
    assert res["success"] is True
    assert res["algorithm"] == "kruskal"
    assert res["result"]["summary"]["total_cost"] == 10
    assert set(res["result"]["details"]["mst_edges"]) == {"e1", "e2", "e4", "e5"}
    assert len(res["result"]["details"]["edge_list"]) == 4


def test_kruskal_steps_exist():
    res = run_kruskal(GRAPH_5, {})
    steps = res["visualization"]["steps"]
    assert len(steps) > 0
    # Chaque étape doit avoir les champs requis par le contrat
    for s in steps:
        assert "index" in s
        assert "title" in s
        assert "description" in s
        assert "state" in s
        state = s["state"]
        for field in [
            "highlighted_nodes", "highlighted_edges", "visited_nodes",
            "selected_nodes", "selected_edges", "node_labels",
            "edge_labels", "node_colors", "edge_colors", "extra",
        ]:
            assert field in state, f"Champ manquant dans state : {field}"


def test_kruskal_result_graph():
    res = run_kruskal(GRAPH_5, {})
    rg = res["visualization"]["result_graph"]
    assert "highlighted_nodes" in rg
    assert "highlighted_edges" in rg
    assert len(rg["highlighted_edges"]) == 4


def test_kruskal_meta():
    res = run_kruskal(GRAPH_5, {})
    meta = res["meta"]
    assert meta["step_count"] == len(res["visualization"]["steps"])
    assert meta["execution_time_ms"] >= 0


def test_kruskal_single_node():
    """Un graphe à un seul sommet → ACM vide, coût 0."""
    g = {
        "directed": False, "weighted": True,
        "nodes": [{"id": "A", "label": "A"}],
        "edges": [],
    }
    res = run_kruskal(g, {})
    assert res["success"] is True
    assert res["result"]["summary"]["total_cost"] == 0
    assert res["result"]["details"]["mst_edges"] == []


def test_kruskal_disconnected_graph():
    """Graphe non connexe → avertissement + forêt couvrante (Kruskal l'accepte)."""
    g = {
        "directed": False, "weighted": True,
        "nodes": [
            {"id": "A"}, {"id": "B"}, {"id": "C"}, {"id": "D"},
        ],
        "edges": [
            {"id": "e1", "source": "A", "target": "B", "weight": 1},
            {"id": "e2", "source": "C", "target": "D", "weight": 2},
        ],
    }
    res = run_kruskal(g, {})
    assert res["success"] is True
    assert len(res["meta"]["warnings"]) > 0
    assert res["result"]["summary"]["total_cost"] == 3


# ──────────────────────────────────────────────────────────────────────────────
#  Kruskal — cas d'erreur
# ──────────────────────────────────────────────────────────────────────────────

def test_kruskal_directed_graph():
    g = dict(GRAPH_5)
    g["directed"] = True
    res = run_kruskal(g, {})
    assert res["success"] is False
    assert res["error"]["code"] == "INVALID_GRAPH_FOR_ALGORITHM"


def test_kruskal_unweighted_graph():
    g = dict(GRAPH_5)
    g["weighted"] = False
    # On enlève les poids pour simuler
    edges_no_weight = [
        {"id": e["id"], "source": e["source"], "target": e["target"]}
        for e in GRAPH_5["edges"]
    ]
    g = {**GRAPH_5, "weighted": False, "edges": edges_no_weight}
    res = run_kruskal(g, {})
    assert res["success"] is False


def test_kruskal_empty_nodes():
    g = {"directed": False, "weighted": True, "nodes": [], "edges": []}
    res = run_kruskal(g, {})
    assert res["success"] is False
    assert res["error"]["code"] == "INVALID_GRAPH"


def test_kruskal_missing_node_ref():
    g = {
        "directed": False, "weighted": True,
        "nodes": [{"id": "A"}, {"id": "B"}],
        "edges": [{"id": "e1", "source": "A", "target": "Z", "weight": 1}],
    }
    res = run_kruskal(g, {})
    assert res["success"] is False
    assert res["error"]["code"] == "NODE_NOT_FOUND"


# ──────────────────────────────────────────────────────────────────────────────
#  Prim — cas normaux
# ──────────────────────────────────────────────────────────────────────────────

def test_prim_basic():
    res = run_prim(GRAPH_5, {"start_node": "A"})
    assert res["success"] is True
    assert res["algorithm"] == "prim"
    assert res["result"]["summary"]["total_cost"] == 10
    assert len(res["result"]["details"]["mst_edges"]) == 4


def test_prim_same_cost_as_kruskal():
    """Prim et Kruskal doivent donner le même coût total."""
    r_k = run_kruskal(GRAPH_5, {})
    r_p = run_prim(GRAPH_5, {"start_node": "A"})
    assert r_k["result"]["summary"]["total_cost"] == r_p["result"]["summary"]["total_cost"]


def test_prim_no_start_node_defaults():
    """Sans start_node, Prim prend le premier sommet."""
    res = run_prim(GRAPH_5, {})
    assert res["success"] is True
    assert res["result"]["summary"]["total_cost"] == 10


def test_prim_different_start():
    """Partir d'un sommet différent doit donner le même coût."""
    res = run_prim(GRAPH_5, {"start_node": "C"})
    assert res["success"] is True
    assert res["result"]["summary"]["total_cost"] == 10


def test_prim_steps_exist():
    res = run_prim(GRAPH_5, {"start_node": "A"})
    steps = res["visualization"]["steps"]
    assert len(steps) > 0
    for s in steps:
        assert "index" in s
        assert "title" in s
        assert "state" in s
        state = s["state"]
        for field in [
            "highlighted_nodes", "highlighted_edges", "visited_nodes",
            "selected_nodes", "selected_edges", "node_labels",
            "edge_labels", "node_colors", "edge_colors", "extra",
        ]:
            assert field in state


def test_prim_single_node():
    g = {
        "directed": False, "weighted": True,
        "nodes": [{"id": "A", "label": "A"}],
        "edges": [],
    }
    res = run_prim(g, {})
    assert res["success"] is True
    assert res["result"]["summary"]["total_cost"] == 0


def test_prim_disconnected():
    """
    Graphe non connexe → Prim doit échouer avec success=False.
    Prim, contrairement à Kruskal, exige un graphe connexe.
    """
    g = {
        "directed": False, "weighted": True,
        "nodes": [{"id": "A"}, {"id": "B"}, {"id": "C"}, {"id": "D"}],
        "edges": [
            {"id": "e1", "source": "A", "target": "B", "weight": 1},
            {"id": "e2", "source": "C", "target": "D", "weight": 2},
        ],
    }
    res = run_prim(g, {"start_node": "A"})
    assert res["success"] is False
    assert res["error"]["code"] == "INVALID_GRAPH_FOR_ALGORITHM"
    assert res["error"]["details"]["algorithm_requires"] == "connected_graph"
    assert res["error"]["details"]["connected_components_count"] == 2


# ──────────────────────────────────────────────────────────────────────────────
#  Prim — cas d'erreur
# ──────────────────────────────────────────────────────────────────────────────

def test_prim_directed_graph():
    g = dict(GRAPH_5)
    g["directed"] = True
    res = run_prim(g, {})
    assert res["success"] is False
    assert res["error"]["code"] == "INVALID_GRAPH_FOR_ALGORITHM"


def test_prim_invalid_start_node():
    res = run_prim(GRAPH_5, {"start_node": "Z"})
    assert res["success"] is False
    assert res["error"]["code"] == "NODE_NOT_FOUND"


def test_prim_empty_nodes():
    g = {"directed": False, "weighted": True, "nodes": [], "edges": []}
    res = run_prim(g, {})
    assert res["success"] is False


def test_prim_missing_node_ref():
    g = {
        "directed": False, "weighted": True,
        "nodes": [{"id": "A"}, {"id": "B"}],
        "edges": [{"id": "e1", "source": "A", "target": "Z", "weight": 1}],
    }
    res = run_prim(g, {})
    assert res["success"] is False
    assert res["error"]["code"] == "NODE_NOT_FOUND"


# ──────────────────────────────────────────────────────────────────────────────
#  Run direct
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Kruskal ===")
    r = run_kruskal(GRAPH_5, {})
    print(f"  success     : {r['success']}")
    print(f"  total_cost  : {r['result']['summary']['total_cost']}")
    print(f"  mst_edges   : {r['result']['details']['mst_edges']}")
    print(f"  step_count  : {r['meta']['step_count']}")

    print("\n=== Prim (départ A) ===")
    r = run_prim(GRAPH_5, {"start_node": "A"})
    print(f"  success     : {r['success']}")
    print(f"  total_cost  : {r['result']['summary']['total_cost']}")
    print(f"  mst_edges   : {r['result']['details']['mst_edges']}")
    print(f"  step_count  : {r['meta']['step_count']}")

    print("\n=== Prim — graphe non connexe ===")
    g_disco = {
        "directed": False, "weighted": True,
        "nodes": [{"id": "A"}, {"id": "B"}, {"id": "C"}, {"id": "D"}],
        "edges": [
            {"id": "e1", "source": "A", "target": "B", "weight": 1},
            {"id": "e2", "source": "C", "target": "D", "weight": 2},
        ],
    }
    r = run_prim(g_disco, {"start_node": "A"})
    print(f"  success     : {r['success']}")
    print(f"  message     : {r['message']}")
    print(f"  error.code  : {r['error']['code']}")
    print(f"  components  : {r['error']['details']['connected_components_count']}")