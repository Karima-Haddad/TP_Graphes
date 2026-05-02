import type { Graph } from "../types/graph.types";

export async function fetchGraphProperties(graph: Graph) {
    console.log("GRAPH ENVOYÉ À L'API =", graph);
  const response = await fetch("http://localhost:8000/api/graph/properties", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      graph: graph,
    }),
  });

  if (!response.ok) {
    throw new Error("Impossible de récupérer les propriétés du graphe");
  }

  return response.json();
}