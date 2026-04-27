def connected_components(graph):

    nodes = [n["id"] for n in graph["nodes"]]

    adj = {n: [] for n in nodes}

    for e in graph["edges"]:
        u, v = e["source"], e["target"]
        adj[u].append(v)
        adj[v].append(u)  # non orienté

    visited = set()
    components = []
    steps = []

    def dfs(node, comp):
        visited.add(node)
        comp.append(node)

        for neigh in adj[node]:
            if neigh not in visited:
                dfs(neigh, comp)

    for node in nodes:
        if node not in visited:
            comp = []
            dfs(node, comp)
            components.append(comp)

            # STEP pour frontend
            steps.append({
                "title": "Nouvelle composante",
                "description": f"Composante trouvée : {comp}",
                "state": {
                    "visited_nodes": list(visited),
                    "selected_nodes": comp
                }
            })

    return {
        "summary": {
            "count": len(components)
        },
        "details": {
            "components": components
        }
    }, steps
