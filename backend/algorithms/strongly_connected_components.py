# from __future__ import annotations

# import time
# from typing import Any

# try:
#     from backend.models.graph import GraphRequest
#     from backend.utils.response_utils import make_response
# except ModuleNotFoundError:  # pragma: no cover
#     from models.graph import GraphRequest
#     from utils.response_utils import make_response


# # def strongly_connected_components(graph):

#     # nodes = graph["nodes"]

#     # adj = {n: [] for n in nodes}
#     # rev = {n: [] for n in nodes}

#     # for e in graph["edges"]:
#     #     u, v = e["source"], e["target"]
#     #     adj[u].append(v)
#     #     rev[v].append(u)

#     # visited = set()
#     # stack = []

#     # def dfs1(node):
#     #     visited.add(node)
#     #     for neigh in adj[node]:
#     #         if neigh not in visited:
#     #             dfs1(neigh)
#     #     stack.append(node)

#     # for n in nodes:
#     #     if n not in visited:
#     #         dfs1(n)

#     # visited.clear()
#     # components = []

#     # def dfs2(node, comp):
#     #     visited.add(node)
#     #     comp.append(node)

#     #     for neigh in rev[node]:
#     #         if neigh not in visited:
#     #             dfs2(neigh, comp)

#     # while stack:
#     #     node = stack.pop()
#     #     if node not in visited:
#     #         comp = []
#     #         dfs2(node, comp)
#     #         components.append(comp)

#     # return {
#     #     "summary": {
#     #         "count": len(components)
#     #     },
#     #     "details": {
#     #         "components": components
#     #     }
#     # }

# def strongly_connected_components(graph):
#     nodes = graph["nodes"]

#     adj = {n: [] for n in nodes}
#     rev = {n: [] for n in nodes}

#     for e in graph["edges"]:
#         u, v = e["source"], e["target"]
#         adj[u].append(v)
#         rev[v].append(u)

#     visited = set()
#     stack = []
#     steps = []

#     def dfs1(node):
#         visited.add(node)

#         steps.append({
#             "title": f"DFS 1 : visite de {node}",
#             "description": f"On visite {node} dans le graphe original.",
#             "state": {
#                 "visited_nodes": list(visited),
#                 "selected_nodes": [],
#                 "highlighted_nodes": [node],
#                 "highlighted_edges": []
#             }
#         })

#         for neigh in adj[node]:
#             if neigh not in visited:
#                 steps.append({
#                     "title": f"DFS 1 : exploration {node} → {neigh}",
#                     "description": f"On explore l’arc {node} vers {neigh}.",
#                     "state": {
#                         "visited_nodes": list(visited),
#                         "selected_nodes": [],
#                         "highlighted_nodes": [node, neigh],
#                         "highlighted_edges": []
#                     }
#                 })

#                 dfs1(neigh)

#         stack.append(node)

#         steps.append({
#             "title": f"Empilement de {node}",
#             "description": f"Le sommet {node} est ajouté à la pile après sa visite.",
#             "state": {
#                 "visited_nodes": list(visited),
#                 "selected_nodes": list(stack),
#                 "highlighted_nodes": [node],
#                 "highlighted_edges": []
#             }
#         })

#     for n in nodes:
#         if n not in visited:
#             dfs1(n)

#     visited.clear()
#     components = []

#     steps.append({
#         "title": "Inversion du graphe",
#         "description": "On travaille maintenant sur le graphe inversé.",
#         "state": {
#             "visited_nodes": [],
#             "selected_nodes": [],
#             "highlighted_nodes": [],
#             "highlighted_edges": []
#         }
#     })

#     def dfs2(node, comp):
#         visited.add(node)
#         comp.append(node)

#         steps.append({
#             "title": f"DFS 2 : visite de {node}",
#             "description": f"Le sommet {node} est ajouté à la composante fortement connexe courante.",
#             "state": {
#                 "visited_nodes": list(visited),
#                 "selected_nodes": list(comp),
#                 "highlighted_nodes": [node],
#                 "highlighted_edges": []
#             }
#         })

#         for neigh in rev[node]:
#             if neigh not in visited:
#                 steps.append({
#                     "title": f"DFS 2 : exploration {node} → {neigh}",
#                     "description": f"Dans le graphe inversé, on explore {node} vers {neigh}.",
#                     "state": {
#                         "visited_nodes": list(visited),
#                         "selected_nodes": list(comp),
#                         "highlighted_nodes": [node, neigh],
#                         "highlighted_edges": []
#                     }
#                 })

#                 dfs2(neigh, comp)

#     while stack:
#         node = stack.pop()

#         if node not in visited:
#             comp = []

#             steps.append({
#                 "title": "Nouvelle CFC",
#                 "description": f"On démarre une nouvelle composante fortement connexe depuis {node}.",
#                 "state": {
#                     "visited_nodes": list(visited),
#                     "selected_nodes": [],
#                     "highlighted_nodes": [node],
#                     "highlighted_edges": []
#                 }
#             })

#             dfs2(node, comp)
#             components.append(comp)

#             steps.append({
#                 "title": "CFC terminée",
#                 "description": f"Composante fortement connexe trouvée : {comp}",
#                 "state": {
#                     "visited_nodes": list(visited),
#                     "selected_nodes": list(comp),
#                     "highlighted_nodes": list(comp),
#                     "highlighted_edges": []
#                 }
#             })

#     return {
#         "summary": {
#             "count": len(components)
#         },
#         "details": {
#             "components": components
#         }
#     }, steps

# def run_strongly_connected_components(graph: GraphRequest) -> dict[str, Any]:
#     """Run strongly connected components algorithm with proper response format."""
#     started_at = time.perf_counter()
#     try:
#         result, steps = strongly_connected_components(graph.model_dump())
        
#         steps = []
#         for comp in result['details']['components']:
#             steps.append({
#                 "title": "Composante fortement connexe",
#                 "description": f"Composante trouvée : {comp}",
#                 "state": {
#                     "selected_nodes": comp
#                 }
#             })
        
#         return make_response(
#             success=True,
#             algorithm="strongly_connected_components",
#             message=f"Trouvé {result['summary']['count']} composante(s) fortement connexe(s)",
#             execution_time_ms=(time.perf_counter() - started_at) * 1000,
#             result=result,
#             steps=steps
#         )
#     except Exception as e:
#         return make_response(
#             success=False,
#             algorithm="strongly_connected_components",
#             message=f"Erreur: {str(e)}",
#             execution_time_ms=(time.perf_counter() - started_at) * 1000,
#             error=str(e)
#         )



from __future__ import annotations

import time
from typing import Any

try:
    from backend.models.graph import GraphRequest
    from backend.utils.response_utils import make_response
except ModuleNotFoundError:
    from models.graph import GraphRequest
    from utils.response_utils import make_response


def get_node_id(node):
    return node["id"] if isinstance(node, dict) else node


def get_edge_id(edge):
    return edge.get("id") or f"{edge['source']}-{edge['target']}"


def strongly_connected_components(graph):
    nodes = [get_node_id(n) for n in graph["nodes"]]
    edges = graph["edges"]

    adj = {n: [] for n in nodes}
    rev = {n: [] for n in nodes}

    for e in edges:
        u, v = e["source"], e["target"]
        edge_id = get_edge_id(e)

        adj[u].append((v, edge_id))
        rev[v].append((u, edge_id))

    visited = set()
    stack = []
    steps = []

    def add_step(title, description, highlighted_nodes=None,
                 highlighted_edges=None, selected_nodes=None,
                 selected_edges=None, extra=None):
        steps.append({
            "title": title,
            "description": description,
            "state": {
                "visited_nodes": list(visited),
                "selected_nodes": selected_nodes or [],
                "selected_edges": selected_edges or [],
                "highlighted_nodes": highlighted_nodes or [],
                "highlighted_edges": highlighted_edges or [],
                "node_labels": {},
                "edge_labels": {},
                "extra": extra or {}
            }
        })

    def dfs1(node):
        visited.add(node)

        add_step(
            title=f"Phase 1 — Visite de {node}",
            description=(
                f"Dans le graphe original, on visite {node}. "
                f"L’objectif de cette première phase est de calculer l’ordre de fin."
            ),
            highlighted_nodes=[node],
            selected_nodes=[],
            selected_edges=[],
            extra={
                "phase": 1,
                "current_node": node,
                "stack": list(stack)
            }
        )

        for neigh, edge_id in adj[node]:
            add_step(
                title=f"Phase 1 — Examen de l’arc {node} → {neigh}",
                description=(
                    f"On vérifie si le voisin {neigh} a déjà été visité "
                    f"dans le graphe original."
                ),
                highlighted_nodes=[node, neigh],
                highlighted_edges=[edge_id],
                selected_nodes=[],
                selected_edges=[],
                extra={
                    "phase": 1,
                    "current_node": node,
                    "neighbor": neigh,
                    "stack": list(stack)
                }
            )

            if neigh not in visited:
                add_step(
                    title=f"Phase 1 — Exploration vers {neigh}",
                    description=(
                        f"{neigh} n’est pas encore visité. "
                        f"On continue le DFS depuis {node} vers {neigh}."
                    ),
                    highlighted_nodes=[node, neigh],
                    highlighted_edges=[edge_id],
                    extra={
                        "phase": 1,
                        "current_node": node,
                        "next_node": neigh,
                        "stack": list(stack)
                    }
                )

                dfs1(neigh)

            else:
                add_step(
                    title=f"Phase 1 — {neigh} déjà visité",
                    description=(
                        f"{neigh} est déjà visité. "
                        f"On ne relance pas DFS sur ce sommet."
                    ),
                    highlighted_nodes=[node, neigh],
                    highlighted_edges=[edge_id],
                    extra={
                        "phase": 1,
                        "current_node": node,
                        "already_visited": neigh,
                        "stack": list(stack)
                    }
                )

        stack.append(node)

        add_step(
            title=f"Empilement de {node}",
            description=(
                f"Tous les voisins de {node} ont été traités. "
                f"On empile {node} selon son ordre de fin."
            ),
            highlighted_nodes=[node],
            selected_nodes=list(stack),
            extra={
                "phase": 1,
                "current_node": node,
                "stack": list(stack)
            }
        )

    for node in nodes:
        if node not in visited:
            add_step(
                title="Phase 1 — Nouveau départ DFS",
                description=(
                    f"Le sommet {node} n’est pas encore visité. "
                    f"On démarre un nouveau DFS dans le graphe original."
                ),
                highlighted_nodes=[node],
                extra={
                    "phase": 1,
                    "start_node": node,
                    "stack": list(stack)
                }
            )

            dfs1(node)

    visited.clear()
    components = []

    add_step(
        title="Phase 2 — Graphe transposé",
        description=(
            "On inverse tous les arcs du graphe. "
            "Ensuite, on dépile les sommets pour trouver les composantes fortement connexes."
        ),
        highlighted_nodes=[],
        highlighted_edges=[],
        selected_nodes=[],
        selected_edges=[],
        extra={
            "phase": 2,
            "stack": list(stack)
        }
    )

    def dfs2(node, comp, comp_edges):
        visited.add(node)
        comp.append(node)

        add_step(
            title=f"Phase 2 — Ajout de {node}",
            description=(
                f"Dans le graphe transposé, {node} est atteint. "
                f"Il est ajouté à la CFC courante."
            ),
            highlighted_nodes=[node],
            selected_nodes=list(comp),
            selected_edges=list(comp_edges),
            extra={
                "phase": 2,
                "current_node": node,
                "component": list(comp),
                "stack": list(stack)
            }
        )

        for neigh, edge_id in rev[node]:
            add_step(
                title=f"Phase 2 — Examen de l’arc inversé {node} → {neigh}",
                description=(
                    f"Dans le graphe transposé, on vérifie si {neigh} "
                    f"appartient à la même composante fortement connexe."
                ),
                highlighted_nodes=[node, neigh],
                highlighted_edges=[edge_id],
                selected_nodes=list(comp),
                selected_edges=list(comp_edges),
                extra={
                    "phase": 2,
                    "current_node": node,
                    "neighbor": neigh,
                    "component": list(comp),
                    "stack": list(stack)
                }
            )

            if neigh not in visited:
                comp_edges.append(edge_id)

                add_step(
                    title=f"Phase 2 — Exploration vers {neigh}",
                    description=(
                        f"{neigh} n’est pas encore visité dans la phase 2. "
                        f"On l’ajoute potentiellement à la même CFC que {node}."
                    ),
                    highlighted_nodes=[node, neigh],
                    highlighted_edges=[edge_id],
                    selected_nodes=list(comp),
                    selected_edges=list(comp_edges),
                    extra={
                        "phase": 2,
                        "current_node": node,
                        "next_node": neigh,
                        "component": list(comp),
                        "stack": list(stack)
                    }
                )

                dfs2(neigh, comp, comp_edges)

            else:
                add_step(
                    title=f"Phase 2 — {neigh} déjà traité",
                    description=(
                        f"{neigh} a déjà été affecté à une composante. "
                        f"On ne le revisite pas."
                    ),
                    highlighted_nodes=[node, neigh],
                    highlighted_edges=[edge_id],
                    selected_nodes=list(comp),
                    selected_edges=list(comp_edges),
                    extra={
                        "phase": 2,
                        "current_node": node,
                        "already_visited": neigh,
                        "component": list(comp),
                        "stack": list(stack)
                    }
                )

    while stack:
        node = stack.pop()

        add_step(
            title=f"Dépilement de {node}",
            description=(
                f"On retire {node} de la pile. "
                f"S’il n’est pas encore visité en phase 2, il démarre une nouvelle CFC."
            ),
            highlighted_nodes=[node],
            selected_nodes=list(stack),
            extra={
                "phase": 2,
                "popped_node": node,
                "stack": list(stack)
            }
        )

        if node not in visited:
            comp = []
            comp_edges = []

            add_step(
                title="Nouvelle composante fortement connexe",
                description=(
                    f"{node} n’a pas encore été affecté à une CFC. "
                    f"On démarre donc un DFS dans le graphe transposé à partir de {node}."
                ),
                highlighted_nodes=[node],
                selected_nodes=[],
                selected_edges=[],
                extra={
                    "phase": 2,
                    "start_node": node,
                    "stack": list(stack)
                }
            )

            dfs2(node, comp, comp_edges)
            components.append(comp)

            add_step(
                title="CFC terminée",
                description=(
                    f"Les sommets {' → '.join(comp)} sont mutuellement atteignables. "
                    f"Ils forment une composante fortement connexe."
                ),
                highlighted_nodes=list(comp),
                highlighted_edges=list(comp_edges),
                selected_nodes=list(comp),
                selected_edges=list(comp_edges),
                extra={
                    "phase": 2,
                    "component": list(comp),
                    "stack": list(stack)
                }
            )

    return {
        "summary": {
            "count": len(components)
        },
        "details": {
            "components": components
        }
    }, steps


def run_strongly_connected_components(graph: GraphRequest) -> dict[str, Any]:
    started_at = time.perf_counter()

    try:
        result, steps = strongly_connected_components(graph.model_dump())

        return make_response(
            success=True,
            algorithm="strongly_connected_components",
            message=f"Trouvé {result['summary']['count']} composante(s) fortement connexe(s)",
            execution_time_ms=(time.perf_counter() - started_at) * 1000,
            result=result,
            steps=steps
        )

    except Exception as e:
        return make_response(
            success=False,
            algorithm="strongly_connected_components",
            message=f"Erreur: {str(e)}",
            execution_time_ms=(time.perf_counter() - started_at) * 1000,
            error=str(e)
        )