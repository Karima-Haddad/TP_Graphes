import type { AlgorithmKey } from "../types/algorithm.types";

type BuildExecutionParamsArgs = {
  algorithm: AlgorithmKey;
  sourceNode: string;
  targetNode: string;
};

export function buildExecutionParams({
  algorithm,
  sourceNode,
  targetNode,
}: BuildExecutionParamsArgs): Record<string, unknown> {
  switch (algorithm) {
    case "dijkstra":
    case "bellman-ford":
    case "bellman":
      return {
        source: sourceNode,
        target: targetNode,
      };

    case "prim":
    case "euler":
      return {
        start_node: sourceNode,
      };

    case "kruskal":
    case "connected-components":
    case "strongly-connected-components":
    case "welsh-powell":
      return {};

    default:
      return {};
  }
}