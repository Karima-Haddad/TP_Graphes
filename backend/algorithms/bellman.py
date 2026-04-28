"""
bellman.py — Algorithme de Bellman (version simplifiée pour graphes sans circuit).

Principe :
  - Applicable uniquement si le graphe ne contient pas de circuit (DAG).
  - Initialisation : d(source) = 0, les autres à ∞.
  - À chaque itération, on choisit un sommet x dont TOUS les prédécesseurs sont déjà traités.
  - On calcule d(x) = min sur les prédécesseurs p de [d(p) + w(p,x)]  (équation de Bellman)
  - On marque x comme traité et on continue jusqu'à ce que tous les sommets soient traités.

Pour appliquer cet algorithme, on effectue d'abord un tri topologique du graphe,
ce qui garantit que les prédécesseurs de chaque sommet sont toujours traités avant lui.

Complexité : O(V + E)
"""

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
ALGORITHM = "bellman"


def run(graph_data: dict, params: dict) -> dict:
    """
    Point d'entrée de l'algorithme de Bellman (DAG).
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

    # L'algorithme de Bellman (simplifié) nécessite un graphe orienté sans circuit
    if not graph.directed:
        return build_error_response(
            ALGORITHM, params,
            "L'algorithme de Bellman (simplifié) nécessite un graphe orienté sans circuit.",
            "INVALID_GRAPH_FOR_ALGORITHM",
            details={"algorithm_requires": "directed_acyclic_graph"}
        )

    # ── Tri topologique + détection de cycle ──────────────────────────────
    topo_order, has_cycle = _topological_sort(graph)

    if has_cycle:
        return build_error_response(
            ALGORITHM, params,
            "Le graphe contient un circuit. L'algorithme de Bellman (simplifié) ne s'applique pas.",
            "INVALID_GRAPH_FOR_ALGORITHM",
            details={"algorithm_requires": "acyclic_graph (DAG)"}
        )

    # ── Exécution de l'algorithme de Bellman ──────────────────────────────
    distances, predecessors, steps = _bellman(graph, source, topo_order)

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
            "distance": distance
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


def _topological_sort(graph: Graph) -> tuple[list[str], bool]:
    """
    Tri topologique par l'algorithme de Kahn (basé sur les degrés entrants).
    Retourne (ordre_topologique, has_cycle).
    Si has_cycle est True, l'ordre retourné est incomplet.
    """
    # Calcul du degré entrant de chaque sommet
    in_degree = {node_id: 0 for node_id in graph.nodes}
    for edge in graph.edges.values():
        in_degree[edge.target] += 1

    # File des sommets sans prédécesseur (degré entrant = 0)
    queue = [node_id for node_id, deg in in_degree.items() if deg == 0]
    topo_order = []

    while queue:
        # On choisit le premier sommet disponible (tous ses prédécesseurs sont traités)
        node = queue.pop(0)
        topo_order.append(node)

        # On "retire" ce sommet du graphe en décrémentant les degrés de ses successeurs
        for neighbor, _, _ in graph.get_neighbors(node):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Si tous les sommets ne sont pas dans l'ordre, il y a un cycle
    has_cycle = len(topo_order) != len(graph.nodes)
    return topo_order, has_cycle


def _bellman(graph: Graph, source: str, topo_order: list[str]):
    """
    Cœur de l'algorithme de Bellman sur DAG.
    On traite les sommets dans l'ordre topologique.
    Pour chaque sommet x, on applique l'équation de Bellman :
        d(x) = min sur les prédécesseurs p de [d(p) + w(p, x)]
    Retourne : (distances, predecessors, steps)
    """
    distances = {node_id: INF for node_id in graph.nodes}
    distances[source] = 0
    predecessors = {node_id: None for node_id in graph.nodes}
    treated = []   # Sommets définitivement calculés
    steps = []

    # Étape 0 : Initialisation
    steps.append(make_step(
        index=0,
        title="Initialisation",
        description=f"Distance({source})=0, tous les autres sommets à ∞. Ordre topologique : {topo_order}",
        highlighted_nodes=[source],
        selected_nodes=[source],
        node_labels=format_distances_as_labels(distances),
        extra={"topological_order": topo_order, "current_node": source}
    ))

    # Traitement dans l'ordre topologique
    for node in topo_order:
        predecessors_data = graph.get_predecessors(node)

        # Cas source : déjà initialisé à 0, pas de calcul nécessaire
        if node == source:
            treated.append(node)
            continue

        # Si le sommet n'a pas de prédécesseur accessible, il reste à ∞
        if not predecessors_data:
            treated.append(node)
            steps.append(make_step(
                index=len(steps),
                title=f"Traitement de {node}",
                description=f"{node} n'a pas de prédécesseur → distance reste ∞",
                highlighted_nodes=[node],
                visited_nodes=list(treated),
                node_labels=format_distances_as_labels(distances),
                extra={"current_node": node}
            ))
            continue

        # ── Équation de Bellman : d(x) = min[d(p) + w(p,x)] ──────────────
        best_dist = INF
        best_pred = None
        best_edge = None

        for pred_id, weight, edge_id in predecessors_data:
            if distances[pred_id] == INF:
                continue  # Prédécesseur inaccessible, on ignore
            candidate = distances[pred_id] + weight
            if candidate < best_dist:
                best_dist = candidate
                best_pred = pred_id
                best_edge = edge_id

        if best_dist < distances[node]:
            distances[node] = best_dist
            predecessors[node] = best_pred

        treated.append(node)

        steps.append(make_step(
            index=len(steps),
            title=f"Traitement de {node}",
            description=(
                f"d({node}) = d({best_pred}) + w({best_pred},{node}) = {best_dist}"
                if best_pred else f"Aucun prédécesseur accessible → d({node}) reste ∞"
            ),
            highlighted_nodes=[node] + ([best_pred] if best_pred else []),
            highlighted_edges=[best_edge] if best_edge else [],
            visited_nodes=list(treated),
            selected_nodes=list(treated),
            selected_edges=[best_edge] if best_edge else [],
            node_labels=format_distances_as_labels(distances),
            extra={"current_node": node, "best_predecessor": best_pred}
        ))

    return distances, predecessors, steps
