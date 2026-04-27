def strongly_connected_components(graph):

    nodes = [n["id"] for n in graph["nodes"]]

    adj = {n: [] for n in nodes}
    rev = {n: [] for n in nodes}

    for e in graph["edges"]:
        u, v = e["source"], e["target"]
        adj[u].append(v)
        rev[v].append(u)

    visited = set()
    stack = []

    def dfs1(node):
        visited.add(node)
        for neigh in adj[node]:
            if neigh not in visited:
                dfs1(neigh)
        stack.append(node)

    for n in nodes:
        if n not in visited:
            dfs1(n)

    visited.clear()
    components = []

    def dfs2(node, comp):
        visited.add(node)
        comp.append(node)

        for neigh in rev[node]:
            if neigh not in visited:
                dfs2(neigh, comp)

    while stack:
        node = stack.pop()
        if node not in visited:
            comp = []
            dfs2(node, comp)
            components.append(comp)

    return {
        "summary": {
            "count": len(components)
        },
        "details": {
            "components": components
        }
    }
