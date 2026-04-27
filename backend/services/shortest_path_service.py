"""
shortest_path_service.py — Service de dispatch pour les algorithmes de plus court chemin.

Reçoit la requête validée depuis la route, appelle le bon algorithme
et retourne la réponse JSON du contrat.
"""

from algorithms import dijkstra, bellman_ford, bellman
from utils.utils import build_error_response

# Registre des algorithmes disponibles
SHORTEST_PATH_ALGORITHMS = {
    "dijkstra":     dijkstra.run,
    "bellman-ford": bellman_ford.run,
    "bellman":      bellman.run,
}


def run_shortest_path(algorithm_name: str, graph_data: dict, params: dict) -> dict:
    """
    Dispatch vers le bon algorithme de plus court chemin.

    Args:
        algorithm_name : identifiant de l'algorithme ("dijkstra", "bellman-ford", "bellman")
        graph_data     : structure du graphe conforme au contrat
        params         : paramètres de l'algorithme (source, target)

    Returns:
        Réponse JSON conforme au contrat (succès ou erreur)
    """
    name = algorithm_name.lower()

    if name not in SHORTEST_PATH_ALGORITHMS:
        return build_error_response(
            algorithm=name or "unknown",
            params=params,
            message=(
                f"Algorithme '{name}' non reconnu parmi les algorithmes de plus court chemin. "
                f"Disponibles : {list(SHORTEST_PATH_ALGORITHMS.keys())}"
            ),
            code="INVALID_PARAMS",
            field="algorithm"
        )

    # Délégation à l'algorithme approprié
    return SHORTEST_PATH_ALGORITHMS[name](graph_data, params)