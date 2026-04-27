"""
Ford-Fulkerson (Edmonds-Karp) — Flot Maximum
=============================================
Implémentation utilisant BFS (Edmonds-Karp) pour garantir
une complexité polynomiale O(V * E²).

Contrat d'entrée :
  algorithm : "ford_fulkerson"
  graph     : { directed, weighted, nodes, edges }
  params    : { source: str, target: str }

Contrat de sortie :
  Voir build_success_response() — même enveloppe que tous les algos.
"""

import time
from collections import defaultdict, deque


# ─────────────────────────────────────────────
#  Structures internes
# ─────────────────────────────────────────────

def build_residual_graph(nodes, edges):
    """
    Construit le graphe résiduel sous forme de dict de dict.
    Retourne aussi un mapping edge_id → (u, v) pour la visualisation.

    residual[u][v] = capacité résiduelle de u → v
    Pour chaque arc forward (u→v, cap), on ajoute aussi (v→u, 0) si absent.
    """
    residual = defaultdict(lambda: defaultdict(int))
    edge_map = {}          # (u, v) → edge_id  (arcs originaux seulement)
    flow_map = {}          # (u, v) → flot actuel

    for edge in edges:
        u = edge["source"]
        v = edge["target"]
        cap = edge.get("weight", 1)
        eid = edge["id"]

        residual[u][v] += cap          # arc forward
        if residual[v][u] == 0:        # arc backward (si pas déjà un arc réel)
            residual[v][u] = 0

        edge_map[(u, v)] = eid
        flow_map[(u, v)] = 0
        if (v, u) not in flow_map:
            flow_map[(v, u)] = 0

    return residual, edge_map, flow_map


def bfs_find_path(residual, source, target):
    """
    BFS dans le graphe résiduel.
    Retourne (parent_map, path_found).
    parent_map[v] = u signifie qu'on arrive à v depuis u.
    """
    visited = {source}
    parent = {source: None}
    queue = deque([source])

    while queue:
        u = queue.popleft()
        for v, cap in residual[u].items():
            if v not in visited and cap > 0:
                visited.add(v)
                parent[v] = u
                if v == target:
                    return parent, True
                queue.append(v)

    return parent, False


def reconstruct_path(parent, source, target):
    """Reconstruit le chemin depuis parent_map → liste de nœuds."""
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path


# ─────────────────────────────────────────────
#  Algorithme principal
# ─────────────────────────────────────────────

def run_ford_fulkerson(graph, params):
    """
    Exécute Ford-Fulkerson (variante Edmonds-Karp).

    Retourne (max_flow, flow_on_edges, steps, augmenting_paths)
      - max_flow        : int, valeur du flot maximum
      - flow_on_edges   : dict (u,v) → flot final
      - steps           : liste d'étapes au format contrat
      - augmenting_paths: liste de chemins augmentants trouvés
    """
    nodes_data = graph["nodes"]
    edges_data = graph["edges"]
    source = params["source"]
    target   = params["target"]

    node_ids = [n["id"] for n in nodes_data]

    # Validation rapide
    if source not in node_ids:
        raise ValueError(f"NODE_NOT_FOUND: le nœud source '{source}' n'existe pas.")
    if target not in node_ids:
        raise ValueError(f"NODE_NOT_FOUND: le nœud puits '{target}' n'existe pas.")
    if source == target:
        raise ValueError("INVALID_PARAMS: source et puits ne peuvent pas être identiques.")

    residual, edge_map, flow_map = build_residual_graph(node_ids, edges_data)

    max_flow = 0
    steps = []
    augmenting_paths = []
    iteration = 0

    # ── Étape 0 : initialisation ────────────────────────────────────────
    steps.append({
        "index": 0,
        "title": "Initialisation",
        "description": (
            f"Graphe résiduel initialisé. "
            f"Tous les flots sont à 0. "
            f"Source = {source}, Puits = {target}."
        ),
        "state": {
            "highlighted_nodes": [source, target],
            "highlighted_edges": [],
            "visited_nodes": [],
            "selected_nodes": [source, target],
            "selected_edges": [],
            "node_labels": {n["id"]: "0" for n in nodes_data},
            "edge_labels": {
                e["id"]: f"0/{e.get('weight', 1)}"
                for e in edges_data
            },
            "node_colors": {
                source: "#4f46e5",
                target:   "#15803d"
            },
            "edge_colors": {},
            "extra": {
                "max_flow_so_far": 0,
                "iteration": 0
            }
        }
    })

    # ── Boucle principale ───────────────────────────────────────────────
    while True:
        parent, found = bfs_find_path(residual, source, target)

        if not found:
            # Plus de chemin augmentant → flot maximum atteint
            steps.append({
                "index": len(steps),
                "title": "Flot maximum atteint",
                "description": (
                    f"Aucun chemin augmentant trouvé de {source} à {target}. "
                    f"Le flot maximum est {max_flow}."
                ),
                "state": {
                    "highlighted_nodes": [source, target],
                    "highlighted_edges": _get_saturated_edges(flow_map, edge_map, edges_data),
                    "visited_nodes": node_ids,
                    "selected_nodes": [source, target],
                    "selected_edges": [],
                    "node_labels": {n["id"]: str(max_flow) if n["id"] == source else "" for n in nodes_data},
                    "edge_labels": _build_edge_labels(flow_map, edges_data),
                    "node_colors": {source: "#4f46e5", target: "#15803d"},
                    "edge_colors": {},
                    "extra": {
                        "max_flow_so_far": max_flow,
                        "iteration": iteration
                    }
                }
            })
            break

        # Chemin trouvé → calculer la capacité minimale (goulot)
        path = reconstruct_path(parent, source, target)
        path_flow = float("inf")
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            path_flow = min(path_flow, residual[u][v])

        # Obtenir les edge_ids du chemin pour la visualisation
        path_edge_ids = _path_to_edge_ids(path, edge_map, edges_data)

        iteration += 1
        augmenting_paths.append({
            "iteration": iteration,
            "path": path,
            "flow": path_flow
        })

        # ── Étape : chemin augmentant trouvé ────────────────────────────
        steps.append({
            "index": len(steps),
            "title": f"Itération {iteration} — Chemin trouvé",
            "description": (
                f"Chemin augmentant : {' → '.join(path)}. "
                f"Capacité résiduelle minimale (goulot) = {path_flow}."
            ),
            "state": {
                "highlighted_nodes": path,
                "highlighted_edges": path_edge_ids,
                "visited_nodes": [],
                "selected_nodes": [source, target],
                "selected_edges": path_edge_ids,
                "node_labels": {},
                "edge_labels": _build_edge_labels(flow_map, edges_data),
                "node_colors": {source: "#4f46e5", target: "#15803d"},
                "edge_colors": {eid: "#f59e0b" for eid in path_edge_ids},
                "extra": {
                    "max_flow_so_far": max_flow,
                    "path_flow": path_flow,
                    "iteration": iteration
                }
            }
        })

        # Mettre à jour le graphe résiduel et les flots
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            # Mettre à jour flow_map (uniquement pour les arcs originaux)
            if (u, v) in flow_map:
                flow_map[(u, v)] += path_flow
            if (v, u) in flow_map:
                flow_map[(v, u)] -= path_flow

        max_flow += path_flow

        # ── Étape : mise à jour des flots ───────────────────────────────
        steps.append({
            "index": len(steps),
            "title": f"Itération {iteration} — Mise à jour des flots",
            "description": (
                f"Flot augmenté de {path_flow} sur le chemin. "
                f"Flot total actuel = {max_flow}."
            ),
            "state": {
                "highlighted_nodes": path,
                "highlighted_edges": path_edge_ids,
                "visited_nodes": [],
                "selected_nodes": [source, target],
                "selected_edges": path_edge_ids,
                "node_labels": {},
                "edge_labels": _build_edge_labels(flow_map, edges_data),
                "node_colors": {source: "#4f46e5", target: "#15803d"},
                "edge_colors": {eid: "#0d9488" for eid in path_edge_ids},
                "extra": {
                    "max_flow_so_far": max_flow,
                    "path_flow": path_flow,
                    "iteration": iteration
                }
            }
        })

    return max_flow, flow_map, steps, augmenting_paths


# ─────────────────────────────────────────────
#  Helpers visualisation
# ─────────────────────────────────────────────

def _path_to_edge_ids(path, edge_map, edges_data):
    """Convertit une liste de nœuds en liste d'edge_ids."""
    result = []
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        if (u, v) in edge_map:
            result.append(edge_map[(u, v)])
        elif (v, u) in edge_map:
            result.append(edge_map[(v, u)])
    return result


def _build_edge_labels(flow_map, edges_data):
    """Construit les labels d'arêtes sous forme flot/capacité."""
    labels = {}
    for edge in edges_data:
        u = edge["source"]
        v = edge["target"]
        cap = edge.get("weight", 1)
        f = flow_map.get((u, v), 0)
        labels[edge["id"]] = f"{f}/{cap}"
    return labels


def _get_saturated_edges(flow_map, edge_map, edges_data):
    """Retourne les ids des arêtes saturées (flot == capacité)."""
    saturated = []
    for edge in edges_data:
        u = edge["source"]
        v = edge["target"]
        cap = edge.get("weight", 1)
        f = flow_map.get((u, v), 0)
        if f >= cap:
            saturated.append(edge["id"])
    return saturated


# ─────────────────────────────────────────────
#  Construction de la réponse finale (contrat)
# ─────────────────────────────────────────────

def build_success_response(graph, params, max_flow, flow_map, steps, augmenting_paths, exec_time_ms):
    """
    Construit la réponse JSON finale selon le contrat GraphLab.
    """
    edges_data = graph["edges"]
    source = params["source"]
    target   = params["target"]

    # Arêtes avec flot > 0 (utilisées)
    used_edge_ids = []
    flow_details  = {}
    for edge in edges_data:
        u = edge["source"]
        v = edge["target"]
        f = flow_map.get((u, v), 0)
        flow_details[edge["id"]] = {
            "flow":     max(f, 0),
            "capacity": edge.get("weight", 1),
            "source":   u,
            "target":   v
        }
        if f > 0:
            used_edge_ids.append(edge["id"])

    # Nœuds sur un chemin augmentant (tous ceux touchés)
    all_path_nodes = set()
    for ap in augmenting_paths:
        all_path_nodes.update(ap["path"])

    return {
        "success":   True,
        "algorithm": "ford_fulkerson",
        "message":   "Exécution réussie",
        "params": {
            "source": source,
            "target":   target
        },
        "result": {
            "summary": {
                "max_flow":          max_flow,
                "source":            source,
                "target":              target,
                "augmenting_paths":  len(augmenting_paths)
            },
            "details": {
                "flow_on_edges": flow_details,
                "augmenting_paths": augmenting_paths
            }
        },
        "visualization": {
            "result_graph": {
                "highlighted_nodes": list(all_path_nodes),
                "highlighted_edges": used_edge_ids,
                "node_colors": {
                    source: "#4f46e5",
                    target:   "#15803d"
                },
                "edge_colors": {eid: "#0d9488" for eid in used_edge_ids},
                "node_labels": {},
                "edge_labels": _build_edge_labels(flow_map, edges_data)
            },
            "steps": steps
        },
        "meta": {
            "execution_time_ms": exec_time_ms,
            "step_count":        len(steps),
            "warnings":          []
        },
        "error": None
    }


def build_error_response(algorithm, params, code, message, details=None):
    """Construit une réponse d'erreur selon le contrat GraphLab."""
    return {
        "success":       False,
        "algorithm":     algorithm,
        "message":       message,
        "params":        params,
        "result":        None,
        "visualization": None,
        "meta": {
            "execution_time_ms": 0,
            "step_count":        0,
            "warnings":          []
        },
        "error": {
            "code":    code,
            "type":    "validation_error",
            "details": details or {}
        }
    }


# ─────────────────────────────────────────────
#  Point d'entrée principal
# ─────────────────────────────────────────────

def execute(graph, params):
    """
    Fonction principale appelée par la route Flask.

    Entrée  : graph (dict), params (dict)
    Sortie  : dict (réponse JSON complète selon contrat)
    """
    start = time.time()

    try:
        max_flow, flow_map, steps, augmenting_paths = run_ford_fulkerson(graph, params)
        exec_time = round((time.time() - start) * 1000)

        return build_success_response(
            graph, params, max_flow, flow_map,
            steps, augmenting_paths, exec_time
        )

    except ValueError as e:
        msg = str(e)
        # Extraire le code d'erreur du message
        code = msg.split(":")[0] if ":" in msg else "INVALID_PARAMS"
        return build_error_response("ford_fulkerson", params, code, msg)

    except Exception as e:
        return build_error_response(
            "ford_fulkerson", params,
            "INTERNAL_ERROR",
            f"Erreur interne : {str(e)}"
        )
