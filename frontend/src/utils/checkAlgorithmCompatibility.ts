import type { Graph } from "../types/graph.types";
import type { AlgorithmOption } from "../types/algorithm.types";

export type CompatibilityResult = {
  isCompatible: boolean;
  message: string;
};

export function checkAlgorithmCompatibility(
  graph: Graph,
  algorithm: AlgorithmOption,
  graphProperties?: any
): CompatibilityResult {
  if (algorithm.requiresWeighted && !graph.weighted) {
    return {
      isCompatible: false,
      message: "Cet algorithme nécessite un graphe pondéré.",
    };
  }

  if (algorithm.requiresDirected && !graph.directed) {
    return {
      isCompatible: false,
      message: "Cet algorithme nécessite un graphe orienté.",
    };
  }

  if (algorithm.key === "dijkstra") {
    const hasNegativeWeight = graph.edges.some(
      (edge) => typeof edge.weight === "number" && edge.weight < 0
    );

    if (hasNegativeWeight) {
      return {
        isCompatible: false,
        message: "Dijkstra ne supporte pas les poids négatifs.",
      };
    }
  }

  if (
  (algorithm.key === "prim" || algorithm.key === "kruskal") &&
    graph.directed
  ) {
    return {
      isCompatible: false,
      message: "Prim et Kruskal s’appliquent à un graphe non orienté.",
    };
  }

  if (algorithm.key === "prim" && graphProperties?.result?.summary?.count > 1) {
    return {
      isCompatible: false,
      message: "Prim nécessite un graphe connexe.",
    };
  }


  if (algorithm.key === "ford-fulkerson") {
    const hasNegativeCapacity = graph.edges.some(
      (edge) => typeof edge.weight === "number" && edge.weight < 0
    );

    if (hasNegativeCapacity) {
      return {
        isCompatible: false,
        message: "Ford-Fulkerson ne supporte pas des capacités négatives.",
      };
    }
  }

  if (algorithm.key === "bellman") {
    if (graph.directed) {
      return {
        isCompatible: false,
        message: "Bellman simplifié nécessite un graphe non orienté.",
      };
    }

    if (graphProperties?.result?.has_cycle === true) {
      return {
        isCompatible: false,
        message: "Bellman simplifié nécessite un graphe sans circuit.",
      };
    }
  }

  // const algorithmsThatNeedEdges = [
  //   "dijkstra",
  //   "bellman-ford",
  //   "bellman",
  //   "prim",
  //   "kruskal",
  //   "euler",
  //   "ford-fulkerson",
  // ];

  // if (algorithmsThatNeedEdges.includes(algorithm.key) && graph.edges.length === 0) {
  //   return {
  //     isCompatible: false,
  //     message: "Cet algorithme nécessite au moins une arête.",
  //   };
  // }


  const algorithmsNotApplicableOnEmptyGraph = [
    "dijkstra",
    "bellman-ford",
    "bellman",
    "ford-fulkerson",
  ];

  if (
    graph.nodes.length === 0 &&
    algorithmsNotApplicableOnEmptyGraph.includes(algorithm.key)
  ) {
    return {
      isCompatible: false,
      message: "Cet algorithme n’est pas applicable sur un graphe vide.",
    };
  }




  return {
    isCompatible: true,
    message: "Compatible avec le graphe courant.",
  };
}