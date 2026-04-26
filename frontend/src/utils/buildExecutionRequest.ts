import type { Graph } from "../types/graph.types";
import type { AlgorithmKey } from "../types/algorithm.types";
import type { ExecutionRequest } from "../types/execution.types";
import { buildExecutionParams } from "./buildExecutionParams";

type BuildExecutionRequestArgs = {
  algorithm: AlgorithmKey;
  graph: Graph;
  sourceNode: string;
  targetNode: string;
};

export function buildExecutionRequest({
  algorithm,
  graph,
  sourceNode,
  targetNode,
}: BuildExecutionRequestArgs): ExecutionRequest {
  return {
    algorithm,
    graph,
    params: buildExecutionParams({
      algorithm,
      sourceNode,
      targetNode,
    }),
  };
}