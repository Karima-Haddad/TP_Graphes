import type { Graph } from "./graph.types";
import type { AlgorithmKey } from "./algorithm.types";

export type ExecutionParams = Record<string, unknown>;

export type ExecutionRequest = {
  algorithm: AlgorithmKey;
  graph: Graph;
  params: ExecutionParams;
};