export type AlgorithmKey =
  | "dijkstra"
  | "bellman-ford"
  | "bellman"
  | "kruskal"
  | "prim"
  | "connected-components"
  | "strongly-connected-components"
  | "euler"
  | "welsh-powell";

export type AlgorithmOption = {
  key: AlgorithmKey;
  label: string;
  category: string;
  requiresSource?: boolean;
  requiresTarget?: boolean;
  requiresWeighted?: boolean;
  requiresDirected?: boolean;
  description: string;
};