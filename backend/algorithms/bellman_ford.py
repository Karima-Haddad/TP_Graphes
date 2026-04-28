"""
bellman_ford.py — Algorithme de Bellman-Ford (version file d'attente).

Principe :
  - Initialisation : V = {source}, d(source) = 0, d(autres) = infini
  - Tant que V n'est pas vide :
      • Sélectionner un nœud i dans V et l'en retirer
      • Pour chaque arc (i,j) sortant de i :
          - Si d(j) > d(i) + l(i,j) alors :
              • d(j) = d(i) + l(i,j)   ← mise à jour de l'étiquette
              • Ajouter j à V           ← j doit être retraité

  - Détection de cycle négatif :
      Un compteur suit combien de fois chaque nœud entre dans V.
      Si un nœud entre plus de (|V| - 1) fois → cycle négatif détecté.

Complexité : O(V * E) dans le pire cas, meilleure en pratique.
"""

import time
from collections import deque

try:
    from backend.models.models import Graph
    from backend.utils.utils import (
        reconstruct_path,
        get_path_edges,
        build_success_response,
        build_error_response,
        make_step,
        format_distances_as_labels,
    )
except ModuleNotFoundError:  # pragma: no cover - compatibilite uvicorn depuis backend/
    from models.models import Graph
    from utils.utils import (
        reconstruct_path,
        get_path_edges,
        build_success_response,
        build_error_response,
        make_step,
        format_distances_as_labels,
    )

INF = float('inf')
ALGORITHM = "bellman-ford"


def run(graph_data: dict, params: dict) -> dict:
    """
    Point d'entrée de l'algorithme Bellman-Ford.
    Reçoit le graphe et les paramètres, retourne la réponse JSON du contrat.
    """
    start_time = time.time()
    source = params.get("source")
    target = params.get("target")

    # ── Validation des paramètres ──────────────────────────────────────────
    if not source or not target:
        return build_error_response(
            ALGORITHM, params,
            "Les paramètres 'source' et 'target' sont obligatoires.",
            "INVALID_PARAMS"
        )

    graph = Graph(graph_data)

    if not graph.validate_node(source):
        return build_error_response(
            ALGORITHM, params,
            f"Le nœud source '{source}' n'existe pas dans le graphe.",
            "NODE_NOT_FOUND", field="params.source"
        )
    if not graph.validate_node(target):
        return build_error_response(
            ALGORITHM, params,
            f"Le nœud cible '{target}' n'existe pas dans le graphe.",
            "NODE_NOT_FOUND", field="params.target"
        )

    # ── Exécution de Bellman-Ford ──────────────────────────────────────────
    distances, predecessors, has_negative_cycle, negative_cycle_nodes, steps = _bellman_ford(graph, source)

    if has_negative_cycle:
        return build_error_response(
            ALGORITHM, params,
            "Un cycle de poids négatif a été détecté dans le graphe.",
            "NEGATIVE_CYCLE_DETECTED",
            error_type="algorithm_error",
            details={"negative_cycle_nodes": negative_cycle_nodes}
        )

    # ── Construction du résultat ───────────────────────────────────────────
    path = reconstruct_path(predecessors, source, target)
    path_edges = get_path_edges(graph, path)
    distance = distances[target] if distances[target] != INF else None

    warnings = []
    if distance is None:
        warnings.append(f"Aucun chemin trouvé entre '{source}' et '{target}'.")

    result = {
        "summary": {
            "path": path,
            "distance": distance,
            "has_negative_cycle": False
        },
        "details": {
            "distances": {k: (v if v != INF else None) for k, v in distances.items()},
            "predecessors": predecessors,
            "negative_cycle": []
        }
    }

    visualization = {
        "result_graph": {
            "highlighted_nodes": path,
            "highlighted_edges": path_edges,
            "node_colors": {},
            "edge_colors": {},
            "node_labels": {},
            "edge_labels": {}
        },
        "steps": steps
    }

    return build_success_response(ALGORITHM, params, result, visualization, start_time, warnings)


def _bellman_ford(graph: Graph, source: str):
    """
    Cœur de l'algorithme Bellman-Ford.

    V = file des nœuds à traiter (on démarre avec la source)
    À chaque itération :
      - On retire un nœud i de V
      - On relaxe tous ses arcs sortants (i,j)
      - Si d(j) est amélioré → on met à jour et on ajoute j à V

    Retourne : (distances, predecessors, has_negative_cycle, negative_cycle_nodes, steps)
    """
    nodes = list(graph.nodes.keys())
    n = len(nodes)

    # Initialisation : d(source) = 0, les autres à infini
    distances = {node_id: INF for node_id in nodes}
    distances[source] = 0
    predecessors = {node_id: None for node_id in nodes}

    # Compteur d'entrées dans V pour détecter les cycles négatifs
    entry_count = {node_id: 0 for node_id in nodes}

    # V = file d'attente, on démarre avec la source
    V = deque([source])
    in_queue = {node_id: False for node_id in nodes}
    in_queue[source] = True
    entry_count[source] += 1

    steps = []
    has_negative_cycle = False
    negative_cycle_nodes = []

    # Étape 0 : Initialisation
    steps.append(make_step(
        index=0,
        title="Initialisation",
        description=f"V = {{{source}}}, d({source})=0, tous les autres à ∞",
        highlighted_nodes=[source],
        selected_nodes=[source],
        node_labels=format_distances_as_labels(distances),
        extra={"V": [source]}
    ))

    # ── Tant que V n'est pas vide ──────────────────────────────────────────
    while V:
        # Sélectionner un nœud i dans V et l'en retirer
        i = V.popleft()
        in_queue[i] = False

        relaxed_nodes = []
        relaxed_edges = []

        # Pour chaque arc (i,j) sortant de i
        for j, weight, edge_id in graph.get_neighbors(i):

            # Condition d'optimalité : d(j) > d(i) + l(i,j)
            if distances[i] != INF and distances[i] + weight < distances[j]:

                # Mise à jour de l'étiquette de j
                distances[j] = distances[i] + weight
                predecessors[j] = i
                relaxed_nodes.append(j)
                relaxed_edges.append(edge_id)

                # Ajouter j à V s'il n'y est pas déjà
                if not in_queue[j]:
                    V.append(j)
                    in_queue[j] = True
                    entry_count[j] += 1

                    # Détection cycle négatif : j est entré plus de (n-1) fois
                    if entry_count[j] > n - 1:
                        has_negative_cycle = True
                        if j not in negative_cycle_nodes:
                            negative_cycle_nodes.append(j)

        # Étape : traitement du nœud i
        steps.append(make_step(
            index=len(steps),
            title=f"Traitement de {i}",
            description=(
                f"Mise à jour de {relaxed_nodes}, V = {list(V)}"
                if relaxed_nodes
                else f"Aucune amélioration depuis {i}, V = {list(V)}"
            ),
            highlighted_nodes=[i] + relaxed_nodes,
            highlighted_edges=relaxed_edges,
            selected_nodes=relaxed_nodes,
            node_labels=format_distances_as_labels(distances),
            extra={"current_node": i, "V": list(V)}
        ))

        # Arrêt immédiat si cycle négatif détecté
        if has_negative_cycle:
            steps.append(make_step(
                index=len(steps),
                title="Cycle négatif détecté",
                description=f"Le nœud {negative_cycle_nodes} a été ajouté à V plus de {n-1} fois.",
                highlighted_nodes=negative_cycle_nodes,
                node_colors={nd: "#be123c" for nd in negative_cycle_nodes},
                extra={"has_negative_cycle": True}
            ))
            break

    return distances, predecessors, has_negative_cycle, negative_cycle_nodes, steps
