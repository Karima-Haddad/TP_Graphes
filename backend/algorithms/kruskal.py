"""
Algorithme de Kruskal — Arbre Couvrant Minimal (ACM)
Stratégie : tri des arêtes par poids croissant + Union-Find pour éviter les cycles.
"""

import time
from typing import Any


# ──────────────────────────────────────────────────────────────────────────────
#  Union-Find (Disjoint Set Union)
# ──────────────────────────────────────────────────────────────────────────────

class UnionFind:
    """Structure Union-Find avec compression de chemin et union par rang."""

    def __init__(self, nodes: list[str]):
        self.parent = {n: n for n in nodes}
        self.rank = {n: 0 for n in nodes}

    def find(self, x: str) -> str:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # compression de chemin
        return self.parent[x]

    def union(self, x: str, y: str) -> bool:
        """Fusionne les composantes de x et y. Retourne False si déjà dans la même."""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True

    def same(self, x: str, y: str) -> bool:
        return self.find(x) == self.find(y)


# ──────────────────────────────────────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _node_label(node_id: str, nodes: list[dict]) -> str:
    for n in nodes:
        if n["id"] == node_id:
            return n.get("label", node_id)
    return node_id


def _build_step(
    index: int,
    title: str,
    description: str,
    highlighted_nodes: list[str],
    highlighted_edges: list[str],
    visited_nodes: list[str],
    selected_nodes: list[str],
    selected_edges: list[str],
    node_labels: dict[str, str],
    edge_labels: dict[str, str],
    node_colors: dict[str, str],
    edge_colors: dict[str, str],
    extra: dict[str, Any] | None = None,
) -> dict:
    return {
        "index": index,
        "title": title,
        "description": description,
        "state": {
            "highlighted_nodes": highlighted_nodes,
            "highlighted_edges": highlighted_edges,
            "visited_nodes": visited_nodes,
            "selected_nodes": selected_nodes,
            "selected_edges": selected_edges,
            "node_labels": node_labels,
            "edge_labels": edge_labels,
            "node_colors": node_colors,
            "edge_colors": edge_colors,
            "extra": extra or {},
        },
    }


# ──────────────────────────────────────────────────────────────────────────────
#  Validation
# ──────────────────────────────────────────────────────────────────────────────

def _validate(graph: dict) -> tuple[bool, str, dict | None]:
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    if not nodes:
        return False, "Le graphe ne contient aucun sommet.", {
            "code": "INVALID_GRAPH",
            "type": "validation_error",
            "field": "graph.nodes",
            "details": {},
        }

    if graph.get("directed", False):
        return False, "Kruskal s'applique uniquement aux graphes non orientés.", {
            "code": "INVALID_GRAPH_FOR_ALGORITHM",
            "type": "validation_error",
            "field": "graph.directed",
            "details": {"algorithm_requires": "undirected_graph"},
        }

    if not graph.get("weighted", True):
        return False, "Kruskal nécessite un graphe pondéré.", {
            "code": "INVALID_GRAPH_FOR_ALGORITHM",
            "type": "validation_error",
            "field": "graph.weighted",
            "details": {"algorithm_requires": "weighted_graph"},
        }

    node_ids = {n["id"] for n in nodes}
    for e in edges:
        if e.get("source") not in node_ids:
            return False, f"Source '{e.get('source')}' introuvable.", {
                "code": "NODE_NOT_FOUND",
                "type": "validation_error",
                "field": f"edge {e.get('id')}.source",
                "details": {"missing_node": e.get("source")},
            }
        if e.get("target") not in node_ids:
            return False, f"Cible '{e.get('target')}' introuvable.", {
                "code": "NODE_NOT_FOUND",
                "type": "validation_error",
                "field": f"edge {e.get('id')}.target",
                "details": {"missing_node": e.get("target")},
            }
        if "weight" not in e or e["weight"] is None:
            return False, f"L'arête '{e.get('id')}' n'a pas de poids.", {
                "code": "INVALID_GRAPH",
                "type": "validation_error",
                "field": f"edge {e.get('id')}.weight",
                "details": {},
            }

    return True, "", None


# ──────────────────────────────────────────────────────────────────────────────
#  Algorithme principal
# ──────────────────────────────────────────────────────────────────────────────

def run_kruskal(graph: dict, params: dict) -> dict:
    """
    Exécute Kruskal et retourne la réponse au format contrat GraphLab.

    Paramètres (params) : aucun paramètre obligatoire.
    """
    t_start = time.time()

    # ── Validation ──
    ok, msg, err_detail = _validate(graph)
    if not ok:
        return {
            "success": False,
            "algorithm": "kruskal",
            "message": msg,
            "params": params,
            "result": None,
            "visualization": None,
            "meta": {"execution_time_ms": 0, "step_count": 0, "warnings": []},
            "error": err_detail,
        }

    nodes: list[dict] = graph["nodes"]
    edges: list[dict] = graph["edges"]
    node_ids = [n["id"] for n in nodes]

    # ── Tri des arêtes par poids croissant ──
    sorted_edges = sorted(edges, key=lambda e: e["weight"])

    uf = UnionFind(node_ids)
    mst_edges: list[dict] = []
    mst_edge_ids: list[str] = []
    steps: list[dict] = []
    step_idx = 0
    selected_edges_so_far: list[str] = []
    selected_nodes_so_far: list[str] = []
    warnings: list[str] = []

    # ── Étape 0 : initialisation ──
    steps.append(_build_step(
        index=step_idx,
        title="Initialisation",
        description=(
            f"Tri de {len(sorted_edges)} arête(s) par poids croissant. "
            "Chaque sommet est sa propre composante."
        ),
        highlighted_nodes=[],
        highlighted_edges=[],
        visited_nodes=[],
        selected_nodes=[],
        selected_edges=[],
        node_labels={n["id"]: n.get("label", n["id"]) for n in nodes},
        edge_labels={e["id"]: str(e["weight"]) for e in sorted_edges},
        node_colors={},
        edge_colors={},
        extra={
            "sorted_edges": [e["id"] for e in sorted_edges],
            "mst_edge_count": 0,
            "target_edge_count": len(node_ids) - 1,
        },
    ))
    step_idx += 1

    # ── Étape d'examen de chaque arête ──
    for e in sorted_edges:
        eid = e["id"]
        src, tgt, w = e["source"], e["target"], e["weight"]

        # Étape : on examine cette arête
        steps.append(_build_step(
            index=step_idx,
            title=f"Examen de l'arête {eid}",
            description=(
                f"Arête ({src} — {tgt}, poids {w}). "
                f"Vérification : {src} et {tgt} sont-ils dans la même composante ?"
            ),
            highlighted_nodes=[src, tgt],
            highlighted_edges=[eid],
            visited_nodes=list(selected_nodes_so_far),
            selected_nodes=list(selected_nodes_so_far),
            selected_edges=list(selected_edges_so_far),
            node_labels={n["id"]: n.get("label", n["id"]) for n in nodes},
            edge_labels={e2["id"]: str(e2["weight"]) for e2 in edges},
            node_colors={n: "#4f46e5" for n in selected_nodes_so_far},
            edge_colors={eid: "#f59e0b"},
            extra={
                "current_edge": eid,
                "source": src,
                "target": tgt,
                "weight": w,
                "same_component": uf.same(src, tgt),
            },
        ))
        step_idx += 1

        if uf.same(src, tgt):
            # Cycle détecté → arête rejetée
            steps.append(_build_step(
                index=step_idx,
                title=f"Arête {eid} rejetée (cycle)",
                description=(
                    f"({src} — {tgt}) formerait un cycle. Arête ignorée."
                ),
                highlighted_nodes=[src, tgt],
                highlighted_edges=[eid],
                visited_nodes=list(selected_nodes_so_far),
                selected_nodes=list(selected_nodes_so_far),
                selected_edges=list(selected_edges_so_far),
                node_labels={n["id"]: n.get("label", n["id"]) for n in nodes},
                edge_labels={e2["id"]: str(e2["weight"]) for e2 in edges},
                node_colors={n: "#4f46e5" for n in selected_nodes_so_far},
                edge_colors={eid: "#ef4444"},
                extra={"rejected_edge": eid, "reason": "cycle"},
            ))
            step_idx += 1
        else:
            # Arête acceptée → union des composantes
            uf.union(src, tgt)
            mst_edges.append(e)
            mst_edge_ids.append(eid)

            for nid in [src, tgt]:
                if nid not in selected_nodes_so_far:
                    selected_nodes_so_far.append(nid)
            selected_edges_so_far.append(eid)

            total_so_far = sum(x["weight"] for x in mst_edges)

            steps.append(_build_step(
                index=step_idx,
                title=f"Arête {eid} ajoutée à l'ACM",
                description=(
                    f"({src} — {tgt}, poids {w}) acceptée. "
                    f"Coût partiel : {total_so_far}. "
                    f"ACM : {len(mst_edges)}/{len(node_ids) - 1} arête(s)."
                ),
                highlighted_nodes=[src, tgt],
                highlighted_edges=[eid],
                visited_nodes=list(selected_nodes_so_far),
                selected_nodes=list(selected_nodes_so_far),
                selected_edges=list(selected_edges_so_far),
                node_labels={n["id"]: n.get("label", n["id"]) for n in nodes},
                edge_labels={e2["id"]: str(e2["weight"]) for e2 in edges},
                node_colors={n: "#4f46e5" for n in selected_nodes_so_far},
                edge_colors={eid2: "#15803d" for eid2 in selected_edges_so_far},
                extra={
                    "accepted_edge": eid,
                    "mst_cost_so_far": total_so_far,
                    "mst_edges_so_far": list(mst_edge_ids),
                },
            ))
            step_idx += 1

            # ACM complet ?
            if len(mst_edges) == len(node_ids) - 1:
                break

    # ── Vérification connexité ──
    if len(mst_edges) < len(node_ids) - 1:
        warnings.append(
            "Le graphe n'est pas connexe : l'ACM est une forêt couvrante."
        )

    total_cost = sum(e["weight"] for e in mst_edges)
    mst_node_ids = list(
        {n for e in mst_edges for n in [e["source"], e["target"]]}
    )
    if not mst_edges and node_ids:
        mst_node_ids = node_ids  # graphe sans arêtes

    # ── Étape finale ──
    steps.append(_build_step(
        index=step_idx,
        title="ACM terminé",
        description=(
            f"Arbre couvrant minimal trouvé avec {len(mst_edges)} arête(s) "
            f"et un coût total de {total_cost}."
        ),
        highlighted_nodes=list(mst_node_ids),
        highlighted_edges=list(mst_edge_ids),
        visited_nodes=list(mst_node_ids),
        selected_nodes=list(mst_node_ids),
        selected_edges=list(mst_edge_ids),
        node_labels={n["id"]: n.get("label", n["id"]) for n in nodes},
        edge_labels={e["id"]: str(e["weight"]) for e in edges},
        node_colors={n: "#15803d" for n in mst_node_ids},
        edge_colors={eid2: "#15803d" for eid2 in mst_edge_ids},
        extra={"total_cost": total_cost},
    ))

    exec_ms = round((time.time() - t_start) * 1000, 2)

    return {
        "success": True,
        "algorithm": "kruskal",
        "message": "Exécution réussie",
        "params": params,
        "result": {
            "summary": {
                "total_cost": total_cost,
            },
            "details": {
                "mst_edges": mst_edge_ids,
                "mst_nodes": mst_node_ids,
                "edge_list": [
                    {
                        "id": e["id"],
                        "source": e["source"],
                        "target": e["target"],
                        "weight": e["weight"],
                    }
                    for e in mst_edges
                ],
            },
        },
        "visualization": {
            "result_graph": {
                "highlighted_nodes": mst_node_ids,
                "highlighted_edges": mst_edge_ids,
                "node_colors": {n: "#15803d" for n in mst_node_ids},
                "edge_colors": {eid2: "#15803d" for eid2 in mst_edge_ids},
                "node_labels": {},
                "edge_labels": {e["id"]: str(e["weight"]) for e in mst_edges},
            },
            "steps": steps,
        },
        "meta": {
            "execution_time_ms": exec_ms,
            "step_count": len(steps),
            "warnings": warnings,
        },
        "error": None,
    }