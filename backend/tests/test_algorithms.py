from algorithms.connected_components import connected_components
from algorithms.strongly_connected_components import strongly_connected_components

# ---------- TEST CONNECTED COMPONENTS ----------
graph1 = {
    "nodes": [
        {"id": 1}, {"id": 2}, {"id": 3},
        {"id": 4}, {"id": 5}
    ],
    "edges": [
        {"source": 1, "target": 2},
        {"source": 2, "target": 3},
        {"source": 4, "target": 5}
    ]
}

result_cc, steps = connected_components(graph1)

print("=== CONNECTED COMPONENTS ===")
print(result_cc)
print()

# ---------- TEST SCC ----------
graph2 = {
    "nodes": [
        {"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}
    ],
    "edges": [
        {"source": 1, "target": 2},
        {"source": 2, "target": 1},  # cycle
        {"source": 2, "target": 3},
        {"source": 3, "target": 4},
        {"source": 4, "target": 3}   # cycle
    ]
}

result_scc = strongly_connected_components(graph2)

print("=== STRONGLY CONNECTED COMPONENTS ===")
print(result_scc)
