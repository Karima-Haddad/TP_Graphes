from collections import defaultdict, deque
import sys

sys.setrecursionlimit(10_000)  


class GraphAnalyzer:
    def __init__(self, graph: dict):
        self.graph = graph
        self.nodes = graph.get("nodes", [])
        self.edges = graph.get("edges", [])
        self.directed = graph.get("directed", False)
        self.weighted = graph.get("weighted", False)

        self.adj_list = self.build_adj_list()
        self.adj_matrix = self.build_adj_matrix()

    # --------------------------------------------------
    # 1. Nombre de sommets / arêtes
    # --------------------------------------------------
    def number_of_nodes(self):
        return len(self.nodes)

    def number_of_edges(self):
        return len(self.edges)

    # --------------------------------------------------
    # 2. Degré d'un sommet
    # --------------------------------------------------
    def degree(self, node_id: str):
        deg = 0
        for e in self.edges:
            if e["source"] == node_id:
                deg += 1
            #  éviter de compter deux fois les boucles 
            if e["target"] == node_id and e["target"] != e["source"]:
                deg += 1
        return deg

    def in_degree(self, node_id: str):
        return sum(1 for e in self.edges if e["target"] == node_id)

    def out_degree(self, node_id: str):
        return sum(1 for e in self.edges if e["source"] == node_id)

    def all_degrees(self):
        return {n["id"]: self.degree(n["id"]) for n in self.nodes}

    # --------------------------------------------------
    # 3. Graphe orienté ou non
    # --------------------------------------------------
    def is_directed(self):
        return self.directed

    # --------------------------------------------------
    # 4. Graphe pondéré ou non
    # --------------------------------------------------
    def is_weighted(self):
        # FIX : utiliser self.weighted ET détecter dynamiquement
        return self.weighted or any("weight" in e for e in self.edges)

    # --------------------------------------------------
    # 5. Liste d'adjacence
    # --------------------------------------------------
    def build_adj_list(self):
        adj = defaultdict(list)
        for e in self.edges:
            s, t = e["source"], e["target"]
            w = e.get("weight", 1)
            adj[s].append((t, w))
            if not self.directed:
                adj[t].append((s, w))
        return dict(adj)

    def build_reverse_adj_list(self):
        adj_rev = defaultdict(list)
        for e in self.edges:
            s, t = e["source"], e["target"]
            w = e.get("weight", 1)
            adj_rev[t].append((s, w))
        return dict(adj_rev)

    # --------------------------------------------------
    # 6. Matrice d'adjacence
    # --------------------------------------------------
    def build_adj_matrix(self):
        ids = [n["id"] for n in self.nodes]
        index = {node: i for i, node in enumerate(ids)}
        n = len(ids)
        matrix = [[0] * n for _ in range(n)]
        for e in self.edges:
            if e["source"] in index and e["target"] in index:
                i = index[e["source"]]
                j = index[e["target"]]
                w = e.get("weight", 1)
                matrix[i][j] = w
                if not self.directed:
                    matrix[j][i] = w
        return {"nodes_order": ids, "matrix": matrix}

    # --------------------------------------------------
    # 7. Graphe connexe ou non
    # --------------------------------------------------
    def is_connected(self):
        if not self.nodes:
            return True
        if not self.directed:
            start = self.nodes[0]["id"]
            visited = set()
            queue = deque([start])
            while queue:
                node = queue.popleft()
                if node in visited:
                    continue
                visited.add(node)
                for neigh, _ in self.adj_list.get(node, []):
                    if neigh not in visited:
                        queue.append(neigh)
            return len(visited) == len(self.nodes)
        else:
            return self.is_strongly_connected()

    def is_strongly_connected(self):
        if not self.nodes:
            return True

        # --- Première passe : DFS itératif sur le graphe original ---
        start = self.nodes[0]["id"]
        visited = set()
        finish_stack = []          # ordre de fin de visite
        dfs_stack = [(start, iter(self.adj_list.get(start, [])))]
        visited.add(start)

        # On doit aussi lancer le DFS depuis tous les nœuds non visités
        all_ids = [n["id"] for n in self.nodes]
        pending = deque(all_ids)   # nœuds à essayer comme point de départ

        # DFS itératif complet (Kosaraju passe 1)
        visited2 = set()
        finish_order = []

        def dfs_iterative(adj, sources):
            for src in sources:
                if src in visited2:
                    continue
                stack = [(src, False)]
                while stack:
                    node, returning = stack.pop()
                    if returning:
                        finish_order.append(node)
                        continue
                    if node in visited2:
                        continue
                    visited2.add(node)
                    stack.append((node, True))  # marquer la fin
                    for neigh, _ in adj.get(node, []):
                        if neigh not in visited2:
                            stack.append((neigh, False))

        dfs_iterative(self.adj_list, all_ids)

        # FIX : si tous les nœuds ne sont pas atteints → pas connexe
        if len(visited2) != len(self.nodes):
            return False

        # --- Deuxième passe : DFS sur le graphe renversé ---
        adj_rev = self.build_reverse_adj_list()
        visited3 = set()
        components = 0

        def dfs_reverse(src):
            stack = [src]
            while stack:
                node = stack.pop()
                if node in visited3:
                    continue
                visited3.add(node)
                for neigh, _ in adj_rev.get(node, []):
                    if neigh not in visited3:
                        stack.append(neigh)

        for node in reversed(finish_order):
            if node not in visited3:
                dfs_reverse(node)
                components += 1

        return components == 1

    # --------------------------------------------------
    # 8. Densité du graphe
    # --------------------------------------------------
    def density(self):
        n = self.number_of_nodes()
        m = self.number_of_edges()
        if n <= 1:
            return 0
        if self.directed:
            return m / (n * (n - 1))
        else:
            return (2 * m) / (n * (n - 1))

    # --------------------------------------------------
    # 9. Détection de cycle + dinne le cycle trouve 
    #  logique séparée orienté / non orienté
    # --------------------------------------------------
    def find_cycle(self):
        if self.directed:
            return self._find_cycle_directed()
        else:
            return self._find_cycle_undirected()

    def _find_cycle_directed(self):
        """Détection de cycle dans un graphe orienté (DFS colorié)."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {n["id"]: WHITE for n in self.nodes}
        parent = {}

        def dfs(node):
            color[node] = GRAY
            for neigh, _ in self.adj_list.get(node, []):
                if color[neigh] == GRAY:
                    # Cycle trouvé : reconstruction
                    cycle = [neigh, node]
                    cur = node
                    while cur != neigh and cur in parent:
                        cur = parent[cur]
                        cycle.append(cur)
                    return cycle[::-1]
                if color[neigh] == WHITE:
                    parent[neigh] = node
                    res = dfs(neigh)
                    if res:
                        return res
            color[node] = BLACK
            return None

        for n in self.nodes:
            node_id = n["id"]
            if color[node_id] == WHITE:
                parent[node_id] = None
                res = dfs(node_id)
                if res:
                    return res
        return None

    def _find_cycle_undirected(self):
        """Détection de cycle dans un graphe non orienté."""
        visited = set()
        parent = {}

        def dfs(node, prev):
            visited.add(node)
            for neigh, _ in self.adj_list.get(node, []):
                if neigh not in visited:
                    parent[neigh] = node
                    res = dfs(neigh, node)
                    if res:
                        return res
                elif neigh != prev:
                    # Cycle trouvé
                    cycle = [neigh, node]
                    cur = node
                    while cur != neigh and cur in parent:
                        cur = parent[cur]
                        cycle.append(cur)
                    return cycle[::-1]
            return None

        for n in self.nodes:
            node_id = n["id"]
            if node_id not in visited:
                parent[node_id] = None
                res = dfs(node_id, None)
                if res:
                    return res
        return None

    def has_cycle(self):
        return self.find_cycle() is not None

    # --------------------------------------------------
    # 10. Graphe biparti
    # --------------------------------------------------
    def is_bipartite(self):
        color = {}
        for start in self.nodes:
            s = start["id"]
            if s in color:
                continue
            queue = deque([s])
            color[s] = 0
            while queue:
                node = queue.popleft()
                for neigh, _ in self.adj_list.get(node, []):
                    if neigh not in color:
                        color[neigh] = 1 - color[node]
                        queue.append(neigh)
                    elif color[neigh] == color[node]:
                        return False
        return True

    # --------------------------------------------------
    # 11. Graphe arbre
    # --------------------------------------------------
    def is_tree(self):
        return self.is_connected() and not self.has_cycle()

    # --------------------------------------------------
    # 12. Graphe régulier
    # --------------------------------------------------
    def is_regular(self):
        degrees = list(self.all_degrees().values())
        if not degrees:
            return True
        return len(set(degrees)) == 1

    # --------------------------------------------------
    # 13. Graphe eulérien
    # --------------------------------------------------
    def is_eulerian(self):
        if not self.is_connected():
            return False
        if not self.directed:
            for node in self.nodes:
                if self.degree(node["id"]) % 2 != 0:
                    return False
        else:
            for node in self.nodes:
                node_id = node["id"]
                if self.in_degree(node_id) != self.out_degree(node_id):
                    return False
        return True

    # --------------------------------------------------
    # 14. Propriétés Graphe
    # --------------------------------------------------
    def analyze(self):
        return {
            "nodes_count": self.number_of_nodes(),
            "edges_count": self.number_of_edges(),
            "degrees": self.all_degrees(),
            "is_directed": self.is_directed(),
            "is_weighted": self.is_weighted(),
            "is_connected": self.is_connected(),
            "density": self.density(),
            "has_cycle": self.has_cycle(),
            "cycle": self.find_cycle(),
            "is_bipartite": self.is_bipartite(),
            "is_tree": self.is_tree(),
            "is_regular": self.is_regular(),
            "is_eulerian": self.is_eulerian(),
            "adjacency_list": self.adj_list,
            "adjacency_matrix": self.adj_matrix,
        }

