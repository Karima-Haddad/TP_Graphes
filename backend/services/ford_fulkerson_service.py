"""
Service — Ford-Fulkerson
========================
Couche intermédiaire entre la route Flask et l'algorithme.
Responsabilités :
  - Normaliser le graphe entrant (compléter les champs optionnels)
  - Vérifier la compatibilité du graphe avec Ford-Fulkerson
  - Appeler l'algorithme et retourner la réponse brute
"""


# ─────────────────────────────────────────────
#  Normalisation du graphe
# ─────────────────────────────────────────────

def normalize_graph(graph):
    """
    Complète les champs optionnels manquants pour garantir
    un graphe propre avant de le passer à l'algorithme.

    - Ajoute x=0, y=0 si absents sur les nœuds
    - Ajoute label = id si label absent
    - Ajoute data={} si absent
    - Ajoute weight=1 si graphe non pondéré (capacité uniforme)
    """
    for node in graph["nodes"]:
        node.setdefault("x", 0)
        node.setdefault("y", 0)
        node.setdefault("label", node["id"])
        node.setdefault("data", {})

    for edge in graph["edges"]:
        if not graph.get("weighted", True):
            edge.setdefault("weight", 1)
        edge.setdefault("label", str(edge.get("weight", "")))
        edge.setdefault("data", {})

    return graph


# ─────────────────────────────────────────────
#  Vérification de compatibilité algorithme
# ─────────────────────────────────────────────

def check_compatibility(graph):
    """
    Vérifie que le graphe est compatible avec Ford-Fulkerson.
    Retourne (True, None) si OK, (False, message) sinon.

    Règles Ford-Fulkerson :
      - Doit être orienté (directed = True)
      - Capacités doivent être > 0 si pondéré
    """
    if not graph.get("directed", True):
        return False, (
            "Ford-Fulkerson s'applique à un graphe orienté. "
            "Le graphe fourni est non orienté (directed = false)."
        )

    if graph.get("weighted", True):
        for edge in graph["edges"]:
            w = edge.get("weight")
            if w is not None and w < 0:
                return False, (
                    f"Toutes les capacités doivent être positives. "
                    f"L'arête '{edge['id']}' a une capacité de {w}."
                )

    return True, None


# ─────────────────────────────────────────────
#  Point d'entrée du service
# ─────────────────────────────────────────────

def run(graph, params):
    """
    Entrée du service :
      1. Normalise le graphe
      2. Vérifie la compatibilité
      3. Délègue à l'algorithme
      4. Retourne la réponse JSON complète

    Utilisé par la route Flask.
    """
    try:
        from backend.algorithms.ford_fulkerson import execute, build_error_response
    except ModuleNotFoundError:  # pragma: no cover - compatibilite uvicorn depuis backend/
        from algorithms.ford_fulkerson import execute, build_error_response

    # Étape 1 : normalisation
    graph = normalize_graph(graph)

    # Étape 2 : compatibilité
    ok, reason = check_compatibility(graph)
    if not ok:
        return build_error_response(
            algorithm="ford_fulkerson",
            params=params,
            code="INVALID_GRAPH_FOR_ALGORITHM",
            message=reason
        )

    # ── AJOUT : vérification chemin structurel ──────────────────────────
    from collections import deque

    source = params.get("source")
    target = params.get("target")

    adj = {}
    for e in graph["edges"]:
        adj.setdefault(e["source"], set()).add(e["target"])

    visited = {source}
    queue = deque([source])
    found = False
    while queue:
        u = queue.popleft()
        for v in adj.get(u, []):
            if v == target:
                found = True
                break
            if v not in visited:
                visited.add(v)
                queue.append(v)
        if found:
            break

    if not found:
        return build_error_response(
            algorithm="ford_fulkerson",
            params=params,
            code="NO_PATH",
            message=(
                f"Aucun chemin n'existe entre '{source}' et '{target}' "
                f"dans le graphe. Vérifiez les arêtes et leur orientation."
            )
        )
    # ───────────────────────────────────────────────────────────────────

    # Étape 3 : exécution
    return execute(graph, params)

# ─────────────────────────────────────────────
#  Utilitaire : générer un graphe exemple
# ─────────────────────────────────────────────

def example_graph():
    """
    Retourne un graphe exemple prêt à tester Ford-Fulkerson.
    Utile pour les démos ou les tests manuels.

         S ──10──> A ──10──> T
         │                   ↑
         └──10──> B ──10──┘
                   ↑
         A ──1──> B
    Flot max = 20
    """
    return {
        "algorithm": "ford_fulkerson",
        "graph": {
            "directed": True,
            "weighted": True,
            "nodes": [
                {"id": "S", "label": "S", "x": 60,  "y": 150},
                {"id": "A", "label": "A", "x": 220, "y": 60},
                {"id": "B", "label": "B", "x": 220, "y": 240},
                {"id": "T", "label": "T", "x": 380, "y": 150}
            ],
            "edges": [
                {"id": "e1", "source": "S", "target": "A", "weight": 10, "label": "10"},
                {"id": "e2", "source": "S", "target": "B", "weight": 10, "label": "10"},
                {"id": "e3", "source": "A", "target": "T", "weight": 10, "label": "10"},
                {"id": "e4", "source": "B", "target": "T", "weight": 10, "label": "10"},
                {"id": "e5", "source": "A", "target": "B", "weight": 1,  "label": "1"}
            ]
        },
        "params": {
            "source": "S",
            "target":   "T"
        }
    }
