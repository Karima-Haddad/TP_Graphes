export type VisualizationState = {
  highlighted_nodes: string[];
  highlighted_edges: string[];
  visited_nodes?: string[];
  selected_nodes?: string[];
  selected_edges?: string[];
  node_labels: Record<string, string>;
  edge_labels: Record<string, string>;
  node_colors: Record<string, string>;
  edge_colors: Record<string, string>;
  extra?: Record<string, unknown>;
};

export type ExecutionStep = {
  index: number;
  title: string;
  description: string;
  state: VisualizationState;
};

export type ExecutionSuccessResponse = {
  success: true;
  algorithm: string;
  message: string;
  params: Record<string, unknown>;
  result: {
    summary: Record<string, unknown>;
    details: Record<string, unknown>;
  };
  visualization: {
    result_graph: {
      highlighted_nodes: string[];
      highlighted_edges: string[];
      node_colors: Record<string, string>;
      edge_colors: Record<string, string>;
      node_labels: Record<string, string>;
      edge_labels: Record<string, string>;
    };
    steps: ExecutionStep[];
  };
  meta: {
    execution_time_ms: number;
    step_count: number;
    warnings: string[];
  };
  error: null;
};

export type ExecutionErrorResponse = {
  success: false;
  algorithm: string;
  message: string;
  params: Record<string, unknown>;
  result: null;
  visualization: null;
  meta: {
    execution_time_ms: number;
    step_count: number;
    warnings: string[];
  };
  error: {
    code: string;
    type: string;
    field?: string;
    details?: Record<string, unknown>;
  };
};

export type ExecutionResponse =
  | ExecutionSuccessResponse
  | ExecutionErrorResponse;