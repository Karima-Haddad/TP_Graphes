export type GraphNode = {
  id: string;
  label: string;
  x?: number;
  y?: number;
  data?: Record<string, unknown>;
};

export type GraphEdge = {
  id: string;
  source: string;
  target: string;
  weight?: number;
  label?: string;
  data?: Record<string, unknown>;
};

export type Graph = {
  directed: boolean;
  weighted: boolean;
  nodes: GraphNode[];
  edges: GraphEdge[];
};