"""
Algorithme de Prim — Arbre Couvrant Minimal (ACM)
Stratégie : extension progressive depuis un sommet de départ via un tas min.
"""

import heapq
import time

try:
    from backend.algorithms.connected_components import connected_components as _check_connected
except ModuleNotFoundError:
    from algorithms.connected_components import connected_components as _check_connected


# ──────────────────────────────────────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _build_step(
    index, title, description,
    highlighted_nodes, highlighted_edges,
    visited_nodes, selected_nodes, selected_edges,
    node_labels, edge_labels, node_colors, edge_colors,
    extra=None,
):
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


def _adjacency(nodes, edges):
    """Construit la liste d'adjacence pour graphe non orienté."""
    adj = {n["id"]: [] for n in nodes}
    for e in edges:
        adj[e["source"]].append(e)
        reverse = dict(e)
        reverse["source"], reverse["target"] = e["target"], e["source"]
        adj[e["target"]].append(reverse)
    return adj


# ──────────────────────────────────────────────────────────────────────────────
#  Validation
# ──────────────────────────────────────────────────────────────────────────────

def _validate(graph, params):
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
        return False, "Prim s'applique uniquement aux graphes non orientés.", {
            "code": "INVALID_GRAPH_FOR_ALGORITHM",
            "type": "validation_error",
            "field": "graph.directed",
            "details": {"algorithm_requires": "undirected_graph"},
        }

    if not graph.get("weighted", True):
        return False, "Prim nécessite un graphe pondéré.", {
            "code": "INVALID_GRAPH_FOR_ALGORITHM",
            "type": "validation_error",
            "field": "graph.weighted",
            "details": {"algorithm_requires": "weighted_graph"},
        }

    node_ids = {n["id"] for n in nodes}

    start_node = params.get("start_node")
    if start_node and start_node not in node_ids:
        return False, f"Le sommet de départ '{start_node}' est introuvable.", {
            "code": "NODE_NOT_FOUND",
            "type": "validation_error",
            "field": "params.start_node",
            "details": {"missing_node": start_node},
        }

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

    # ── Vérification de la connexité via le module connected_components ──
    # Un graphe à un seul sommet est connexe par définition.
    if len(nodes) > 1:
        cc_result, _ = _check_connected({"nodes": nodes, "edges": edges})
        nb_components = cc_result["summary"]["count"]
        if nb_components > 1:
            return False, (
                f"Le graphe n'est pas connexe ({nb_components} composantes connexes). "
                "Prim nécessite un graphe connexe."
            ), {
                "code": "INVALID_GRAPH_FOR_ALGORITHM",
                "type": "validation_error",
                "field": "graph",
                "details": {
                    "algorithm_requires": "connected_graph",
                    "connected_components_count": nb_components,
                },
            }

    return True, "", None


# ──────────────────────────────────────────────────────────────────────────────
#  Algorithme principal
# ──────────────────────────────────────────────────────────────────────────────

def run_prim(graph, params):
    """
    Exécute Prim et retourne la réponse au format contrat GraphLab.

    Paramètres (params) :
      - start_node (str, optionnel) : sommet de départ (par défaut le premier nœud)
    """
    t_start = time.time()

    # ── Validation ──
    ok, msg, err_detail = _validate(graph, params)
    if not ok:
        return {
            "success": False,
            "algorithm": "prim",
            "message": msg,
            "params": params,
            "result": None,
            "visualization": None,
            "meta": {"execution_time_ms": 0, "step_count": 0, "warnings": []},
            "error": err_detail,
        }

    nodes  = graph["nodes"]
    edges  = graph["edges"]
    node_ids = [n["id"] for n in nodes]

    # Sommet de départ
    start_node = params.get("start_node") or node_ids[0]

    adj = _adjacency(nodes, edges)

    # ── Structures de suivi ──
    in_mst       = set()
    mst_edges    = []        # arêtes originales acceptées
    mst_edge_ids = []
    steps        = []
    step_idx     = 0
    warnings     = []

    edge_by_id = {e["id"]: e for e in edges}

    # ── Tas min : (poids, edge_id, source, target) ──
    heap = []

    def push_neighbors(node):
        for e in adj[node]:
            if e["target"] not in in_mst:
                heapq.heappush(heap, (e["weight"], e["id"], e["source"], e["target"]))

    def node_label_map():
        return {n["id"]: n.get("label", n["id"]) for n in nodes}

    def edge_label_map():
        return {e["id"]: str(e["weight"]) for e in edges}

    # ── Étape 0 : initialisation ──
    in_mst.add(start_node)
    push_neighbors(start_node)

    steps.append(_build_step(
        index=step_idx,
        title="Initialisation",
        description=(
            f"Départ depuis le sommet '{start_node}'. "
            "Ses voisins sont ajoutés au tas."
        ),
        highlighted_nodes=[start_node],
        highlighted_edges=[],
        visited_nodes=[start_node],
        selected_nodes=[start_node],
        selected_edges=[],
        node_labels=node_label_map(),
        edge_labels=edge_label_map(),
        node_colors={start_node: "#4f46e5"},
        edge_colors={},
        extra={"start_node": start_node, "heap_size": len(heap)},
    ))
    step_idx += 1

    # ── Boucle principale ──
    while heap:
        weight, eid, src, tgt = heapq.heappop(heap)

        if tgt in in_mst:
            # Arête ignorée : sommet déjà dans l'ACM
            steps.append(_build_step(
                index=step_idx,
                title=f"Arête {eid} ignorée",
                description=(
                    f"({src} — {tgt}, poids {weight}) : "
                    f"'{tgt}' est déjà dans l'ACM."
                ),
                highlighted_nodes=[src, tgt],
                highlighted_edges=[eid],
                visited_nodes=list(in_mst),
                selected_nodes=list(in_mst),
                selected_edges=list(mst_edge_ids),
                node_labels=node_label_map(),
                edge_labels=edge_label_map(),
                node_colors={n: "#4f46e5" for n in in_mst},
                edge_colors={eid: "#ef4444"},
                extra={"skipped_edge": eid, "reason": "already_in_mst"},
            ))
            step_idx += 1
            continue

        # Retrouver l'arête originale (direction canonique)
        original_edge = edge_by_id.get(eid)
        if original_edge is None:
            for e in edges:
                if (
                    (e["source"] == src and e["target"] == tgt) or
                    (e["source"] == tgt and e["target"] == src)
                ):
                    original_edge = e
                    break

        in_mst.add(tgt)
        mst_edges.append(original_edge)
        mst_edge_ids.append(original_edge["id"])
        push_neighbors(tgt)

        cost_so_far = sum(e["weight"] for e in mst_edges)

        steps.append(_build_step(
            index=step_idx,
            title=f"Arête {original_edge['id']} ajoutée",
            description=(
                f"({src} — {tgt}, poids {weight}) acceptée. "
                f"Coût partiel : {cost_so_far}. "
                f"ACM : {len(mst_edges)}/{len(node_ids) - 1} arête(s)."
            ),
            highlighted_nodes=[src, tgt],
            highlighted_edges=[original_edge["id"]],
            visited_nodes=list(in_mst),
            selected_nodes=list(in_mst),
            selected_edges=list(mst_edge_ids),
            node_labels=node_label_map(),
            edge_labels=edge_label_map(),
            node_colors={n: "#4f46e5" for n in in_mst},
            edge_colors={e_id: "#15803d" for e_id in mst_edge_ids},
            extra={
                "accepted_edge": original_edge["id"],
                "mst_cost_so_far": cost_so_far,
                "mst_edges_so_far": list(mst_edge_ids),
                "heap_size": len(heap),
            },
        ))
        step_idx += 1

        if len(mst_edges) == len(node_ids) - 1:
            break

    total_cost   = sum(e["weight"] for e in mst_edges)
    mst_node_ids = list(in_mst)

    # ── Étape finale ──
    steps.append(_build_step(
        index=step_idx,
        title="ACM terminé",
        description=(
            f"Arbre couvrant minimal trouvé avec {len(mst_edges)} arête(s) "
            f"et un coût total de {total_cost}."
        ),
        highlighted_nodes=mst_node_ids,
        highlighted_edges=mst_edge_ids,
        visited_nodes=mst_node_ids,
        selected_nodes=mst_node_ids,
        selected_edges=mst_edge_ids,
        node_labels=node_label_map(),
        edge_labels=edge_label_map(),
        node_colors={n: "#15803d" for n in mst_node_ids},
        edge_colors={e_id: "#15803d" for e_id in mst_edge_ids},
        extra={"total_cost": total_cost},
    ))

    exec_ms = round((time.time() - t_start) * 1000, 2)

    return {
        "success": True,
        "algorithm": "prim",
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
                "edge_colors": {e_id: "#15803d" for e_id in mst_edge_ids},
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