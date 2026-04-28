"""
dijkstra.py — Algorithme de Dijkstra (plus court chemin, poids positifs uniquement).

Principe :
  - C'est une version de Bellman-Ford où le nœud choisi dans V est toujours
    celui avec la plus petite distance courante : d(i) = min(j in V) d(j)
  - Initialisation : V = {source}, d(source) = 0, d(autres) = infini
  - Tant que V n'est pas vide :
      • Sélectionner i dans V tel que d(i) = min des distances dans V
      • Retirer i de V
      • Pour chaque arc (i,j) sortant de i :
          - Si d(j) > d(i) + a(i,j) alors :
              • d(j) = d(i) + a(i,j)
              • Ajouter j à V
  - Grâce aux poids positifs, chaque sommet est traité UNE SEULE FOIS.

Complexité : O((V + E) log V) avec un tas min.
"""

import heapq
import time

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
ALGORITHM = "dijkstra"


def run(graph_data: dict, params: dict) -> dict:
    """
    Point d'entrée de l'algorithme Dijkstra.
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

    # Dijkstra exige des poids positifs
    if graph.has_negative_weights():
        neg_edge = next(e for e in graph.edges.values() if e.weight < 0)
        return build_error_response(
            ALGORITHM, params,
            "Le graphe contient un poids négatif, incompatible avec Dijkstra.",
            "INVALID_GRAPH_FOR_ALGORITHM",
            field=f"graph.edges[{neg_edge.id}].weight",
            details={
                "algorithm_requires": "positive_weights_only",
                "received_weight": neg_edge.weight,
                "edge_id": neg_edge.id
            }
        )

    # ── Exécution de Dijkstra ──────────────────────────────────────────────
    distances, predecessors, visited_order, steps = _dijkstra(graph, source, target)

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
            "visited_order": visited_order
        },
        "details": {
            "distances": {k: (v if v != INF else None) for k, v in distances.items()},
            "predecessors": predecessors
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


def _dijkstra(graph: Graph, source: str, target: str):
    """
    Cœur de l'algorithme Dijkstra (version du cours).

    V = ensemble des nœuds à traiter (on démarre avec la source).
    À chaque itération on choisit dans V le nœud i avec d(i) minimal
    → c'est ce qui différencie Dijkstra de Bellman-Ford.
    Grâce aux poids positifs, quand i est retiré de V, d(i) est définitif.

    On utilise un tas min (heapq) pour extraire efficacement le minimum.

    Retourne : (distances, predecessors, visited_order, steps)
    """
    # Initialisation : d(source) = 0, les autres à infini
    distances = {node_id: INF for node_id in graph.nodes}
    distances[source] = 0
    predecessors = {node_id: None for node_id in graph.nodes}

    visited = set()      # Nœuds définitivement traités (retirés de V)
    visited_order = []   # Ordre de visite pour le résultat

    # V représenté par un tas min : (distance, node_id)
    # Chaque entrée dans le tas = nœud ajouté à V
    V = [(0, source)]

    steps = []

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
        # Sélectionner i dans V tel que d(i) = min — extraction du tas min
        current_dist, i = heapq.heappop(V)

        # Si i est déjà traité, on l'ignore (entrée obsolète dans le tas)
        if i in visited:
            continue

        # Retirer i de V → le marquer comme définitivement traité
        visited.add(i)
        visited_order.append(i)

        # Arrêt anticipé : si on vient de traiter la cible, c'est terminé
        if i == target:
            break

        relaxed_nodes = []
        relaxed_edges = []

        # Pour chaque arc (i,j) sortant de i
        for j, weight, edge_id in graph.get_neighbors(i):

            if j in visited:
                continue  # j déjà traité définitivement, on ignore

            # Condition : d(j) > d(i) + a(i,j) ?
            if distances[i] + weight < distances[j]:

                # Mise à jour de d(j)
                distances[j] = distances[i] + weight
                predecessors[j] = i
                relaxed_nodes.append(j)
                relaxed_edges.append(edge_id)

                # Ajouter j à V
                heapq.heappush(V, (distances[j], j))

        # Nœuds actuellement dans V (non encore traités)
        V_display = [node for _, node in V if node not in visited]

        # Étape : traitement du nœud i
        steps.append(make_step(
            index=len(steps),
            title=f"Traitement de {i} (d={current_dist})",
            description=(
                f"d({i})={current_dist} est minimal → traité définitivement. "
                f"Mise à jour de {relaxed_nodes}. V = {V_display}"
                if relaxed_nodes else
                f"d({i})={current_dist} est minimal → traité définitivement. "
                f"Aucune amélioration. V = {V_display}"
            ),
            highlighted_nodes=[i] + relaxed_nodes,
            highlighted_edges=relaxed_edges,
            visited_nodes=list(visited),
            selected_nodes=list(visited),
            node_labels=format_distances_as_labels(distances),
            extra={"current_node": i, "V": V_display}
        ))

    return distances, predecessors, visited_order, steps
