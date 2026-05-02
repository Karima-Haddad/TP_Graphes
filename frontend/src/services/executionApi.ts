import type { ExecutionRequest } from "../types/execution.types";
import type { ExecutionResponse } from "../types/executionResponse.types";
import type { Graph } from "../types/graph.types";

const API_BASE_URL = "http://localhost:8000";

function getEndpoint(algorithm: string): string {
  switch (algorithm) {
    case "dijkstra":
    case "bellman-ford":
    case "bellman":
      return "/api/shortest-path/run";

    case "prim":
    case "kruskal":
      return "/api/mst/run";

    case "connected-components":
      return "/algorithms/connected-components";

    case "strongly-connected-components":
      return "/algorithms/strongly-connected-components";

    case "euler":
      return "/algorithms/euler";

    case "welsh-powell":
      return "/algorithms/welsh-powell";

    case "ford-fulkerson":
      return "/api/algorithms/ford-fulkerson";

    default:
      throw new Error("Algorithme non supporté côté frontend");
  }
}

function toSimpleBackendGraph(graph: Graph) {
  return {
    nodes: graph.nodes.map((node) => node.id),
    edges: graph.edges.map((edge) => ({
      source: edge.source,
      target: edge.target,
    })),
    directed: graph.directed,
  };
}

export async function executeAlgorithm(
  payload: ExecutionRequest
): Promise<ExecutionResponse> {
  const endpoint = getEndpoint(payload.algorithm);

  const simpleGraphAlgorithms = [
    "connected-components",
    "strongly-connected-components",
    "euler",
    "welsh-powell",
  ];

  const requestBody = simpleGraphAlgorithms.includes(payload.algorithm)
    ? toSimpleBackendGraph(payload.graph)
    : payload;

  console.log("Endpoint:", endpoint);
  console.log("Body envoyé:", JSON.stringify(requestBody, null, 2));

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  });

  const data = await response.json();

  if (!response.ok) {
    console.error("Erreur backend:", data);

    throw new Error(
      data?.detail?.[0]?.msg ||
        data?.message ||
        "Erreur lors de l’exécution de l’algorithme"
    );
  }

  return data as ExecutionResponse;
}

export async function fetchGraphProperties(graph: Graph) {
  const response = await fetch(`${API_BASE_URL}/api/graph/properties`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      graph: graph,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    console.error("Graph properties error:", data);

    throw new Error(
      data?.message || "Impossible de récupérer les propriétés du graphe"
    );
  }

  return data;
}

export async function fetchConnectedComponents(graph: Graph) {
  const requestBody = toSimpleBackendGraph({
    ...graph,
    directed: false,
  });

  const response = await fetch(`${API_BASE_URL}/algorithms/connected-components`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  });

  const data = await response.json();

  if (!response.ok) {
    console.error("Connected components error:", data);

    throw new Error(
      data?.message || "Impossible de vérifier la connexité du graphe"
    );
  }

  return data;
}