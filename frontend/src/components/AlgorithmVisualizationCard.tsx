import { useEffect, useMemo, useState } from "react";
import type { Graph } from "../types/graph.types";
import type {
  ExecutionResponse,
  ExecutionStep,
} from "../types/executionResponse.types";

type Props = {
  graph: Graph;
  executionResult: ExecutionResponse | null;
  currentStep: ExecutionStep | null;
  sourceNode?: string;
  targetNode?: string;
};

type DragState = {
  nodeId: string;
  offsetX: number;
  offsetY: number;
} | null;

export function AlgorithmVisualizationCard({
  graph,
  executionResult,
  currentStep,
  sourceNode,
  targetNode,
}: Props) {
  const isLastStep =
    executionResult?.success &&
    currentStep &&
    currentStep.index === executionResult.visualization.steps.length - 1;

  const visualState =
    executionResult?.success && isLastStep
      ? executionResult.visualization.result_graph
      : currentStep
      ? currentStep.state
      : executionResult?.success
      ? executionResult.visualization.result_graph
      : null;


  const nodeColors = visualState?.node_colors ?? {};
  const edgeColors = visualState?.edge_colors ?? {};
  const nodeLabels = visualState?.node_labels ?? {};
  const edgeLabels = visualState?.edge_labels ?? {};

  const [localNodes, setLocalNodes] = useState(graph.nodes);
  const [dragState, setDragState] = useState<DragState>(null);

  useEffect(() => {
    setLocalNodes(graph.nodes);
    }, [graph.nodes]);

  const nodesMap = useMemo(() => {
    return new Map(localNodes.map((node) => [node.id, node]));
  }, [localNodes]);

  const viewBox = useMemo(() => {
    if (localNodes.length === 0) return "0 0 540 300";

    const padding = 80;

    const minX = Math.min(...localNodes.map((node) => node.x ?? 0)) - padding;
    const maxX = Math.max(...localNodes.map((node) => node.x ?? 0)) + padding;
    const minY = Math.min(...localNodes.map((node) => node.y ?? 0)) - padding;
    const maxY = Math.max(...localNodes.map((node) => node.y ?? 0)) + padding;

    return `${minX} ${minY} ${maxX - minX} ${maxY - minY}`;
  }, [localNodes]);

  const getSvgPoint = (event: React.PointerEvent<SVGSVGElement>) => {
    const svg = event.currentTarget;
    //const rect = svg.getBoundingClientRect();

    const svgPoint = svg.createSVGPoint();
    svgPoint.x = event.clientX;
    svgPoint.y = event.clientY;

    const ctm = svg.getScreenCTM();

    if (!ctm) {
      return {
        x: 0,
        y: 0,
      };
    }

    const point = svgPoint.matrixTransform(ctm.inverse());

    return {
      x: point.x,
      y: point.y,
    };
  };

  const handlePointerMove = (event: React.PointerEvent<SVGSVGElement>) => {
    if (!dragState) return;

    const point = getSvgPoint(event);

    setLocalNodes((prev) =>
      prev.map((node) =>
        node.id === dragState.nodeId
          ? {
              ...node,
              x: point.x - dragState.offsetX,
              y: point.y - dragState.offsetY,
            }
          : node
      )
    );
  };

  const handlePointerUp = () => {
    setDragState(null);
  };

  const handlePointerLeave = () => {
    setDragState(null);
  };

  
  const highlightedNodes = new Set(visualState?.highlighted_nodes ?? []);
  const highlightedEdges = new Set(visualState?.highlighted_edges ?? []);

  // const highlightedNodes = currentStep?.state.highlighted_nodes ?? [];
  // const highlightedEdges = currentStep?.state.highlighted_edges ?? [];

  const selectedNodes = currentStep?.state.selected_nodes ?? [];
  const selectedEdges = currentStep?.state.selected_edges ?? [];

  return (
    <div className="card">
      <div className="card-title">Visualisation du résultat</div>

      <div className="visual-zone visual-zone-enhanced">
        <svg
          className="graph-svg"
          viewBox={viewBox}
          preserveAspectRatio="xMidYMid meet"
          onPointerMove={handlePointerMove}
          onPointerUp={handlePointerUp}
          onPointerLeave={handlePointerLeave}
        >
          <defs>
            <radialGradient id="nodeGradientDefault" cx="38%" cy="34%" r="68%">
              <stop offset="0%" stopColor="#e7e9ff" />
              <stop offset="30%" stopColor="#c8d0ff" />
              <stop offset="68%" stopColor="#7b7cf5" />
              <stop offset="100%" stopColor="#4f46e5" />
            </radialGradient>

            <radialGradient id="nodeGradientSource" cx="38%" cy="34%" r="68%">
              <stop offset="0%" stopColor="#dfe4ff" />
              <stop offset="28%" stopColor="#b9c2ff" />
              <stop offset="65%" stopColor="#6f73f4" />
              <stop offset="100%" stopColor="#3730a3" />
            </radialGradient>

            <radialGradient id="nodeGradientTarget" cx="38%" cy="34%" r="68%">
              <stop offset="0%" stopColor="#dfe4ff" />
              <stop offset="28%" stopColor="#a1efc1" />
              <stop offset="65%" stopColor="#45d87a" />
              <stop offset="100%" stopColor="#15803d" />
            </radialGradient>

            <radialGradient
              id="nodeGradientHighlighted"
              cx="38%"
              cy="34%"
              r="68%"
            >
              <stop offset="0%" stopColor="#dfe4ff" />
              <stop offset="28%" stopColor="#bba7ff" />
              <stop offset="65%" stopColor="#9b7ef4" />
              <stop offset="100%" stopColor="#4f46e5" />
            </radialGradient>

            <marker
              id="arrowhead"
              markerWidth="10"
              markerHeight="10"
              refX="8"
              refY="3"
              orient="auto"
              markerUnits="strokeWidth"
            >
              <path d="M0,0 L0,6 L9,3 z" fill="#8f8a83" />
            </marker>
          </defs>

          {graph.edges.map((edge) => {

            const isHighlightedEdge = highlightedEdges.has(edge.id);
            const isSelectedEdge = selectedEdges.includes(edge.id);

            const edgeColor = isHighlightedEdge
              ? "#f97316"
              : isSelectedEdge
              ? "#4f46e5"
              : "#d6d3d1";

            const edgeWidth = isHighlightedEdge || isSelectedEdge ? 4 : 2;

            const source = nodesMap.get(edge.source);
            const target = nodesMap.get(edge.target);

            if (!source || !target) return null;

            const x1 = source.x ?? 0;
            const y1 = source.y ?? 0;
            const x2 = target.x ?? 0;
            const y2 = target.y ?? 0;

            const opposite = graph.edges.some(
                (e) => e.source === edge.target && e.target === edge.source
              );

              const dx = x2 - x1;
              const dy = y2 - y1;
              const length = Math.sqrt(dx * dx + dy * dy) || 1;

              const nodeRadius = 26;

              const startX = x1 + (dx / length) * nodeRadius;
              const startY = y1 + (dy / length) * nodeRadius;
              const endX = x2 - (dx / length) * nodeRadius;
              const endY = y2 - (dy / length) * nodeRadius;

              const curve = opposite ? 35 : 0;
              const normalX = -dy / length;
              const normalY = dx / length;

              const controlX = (startX + endX) / 2 + normalX * curve;
              const controlY = (startY + endY) / 2 + normalY * curve;

              const labelX = opposite
                ? 0.25 * startX + 0.5 * controlX + 0.25 * endX
                : (startX + endX) / 2;

              const labelY = opposite
                ? 0.25 * startY + 0.5 * controlY + 0.25 * endY
                : (startY + endY) / 2;

            const isHighlighted = highlightedEdges.has(edge.id);

            const stroke =
              edgeColors[edge.id] ?? (isHighlighted ? "#4f46e5" : "#d8d3cb");

            const displayedLabel =
              edgeLabels[edge.id] ??
              edge.label ??
              (edge.weight !== undefined ? String(edge.weight) : "");

            return (
              <g key={edge.id}>
                {(() => {
                    const opposite = graph.edges.some(
                      (e) => e.source === edge.target && e.target === edge.source
                    );

                    const dx = x2 - x1;
                    const dy = y2 - y1;
                    const length = Math.sqrt(dx * dx + dy * dy) || 1;

                    const nodeRadius = 26;

                    const startX = x1 + (dx / length) * nodeRadius;
                    const startY = y1 + (dy / length) * nodeRadius;
                    const endX = x2 - (dx / length) * nodeRadius;
                    const endY = y2 - (dy / length) * nodeRadius;

                    const curve = opposite ? 35 : 0;
                    const normalX = -dy / length;
                    const normalY = dx / length;

                    const controlX = (startX + endX) / 2 + normalX * curve;
                    const controlY = (startY + endY) / 2 + normalY * curve;

                    const pathD = opposite
                      ? `M ${startX} ${startY} Q ${controlX} ${controlY} ${endX} ${endY}`
                      : `M ${startX} ${startY} L ${endX} ${endY}`;

                    return (
                      <path
                        d={pathD}
                        fill="none"
                        stroke={edgeColor}
                        strokeWidth={edgeWidth}
                        className={
                          isHighlightedEdge
                            ? "graph-edge path-highlight edge-pulse"
                            : isHighlighted
                            ? "graph-edge path-highlight"
                            : "graph-edge"
                        }
                        markerEnd={graph.directed ? "url(#arrowhead)" : undefined}
                      />
                    );
                  })()}

                {displayedLabel && (
                  <g transform={`translate(${labelX},${labelY - 10})`}>
                    <rect
                      className="graph-edge-badge"
                      x="-16"
                      y="-10"
                      rx="8"
                      ry="8"
                      width="32"
                      height="20"
                    />
                    <text
                      className="graph-edge-badge-text"
                      x="0"
                      y="4"
                      textAnchor="middle"
                    >
                      {displayedLabel}
                    </text>
                  </g>
                )}
              </g>
            );
          })}

          {localNodes.map((node) => {

            const isHighlightedNode = highlightedNodes.has(node.id);
            const isSelectedNode = selectedNodes.includes(node.id);

            const nodeFill = isHighlightedNode
              ? "#fff7ed"
              : isSelectedNode
              ? "#eef2ff"
              : "#ffffff";

            const nodeStroke = isHighlightedNode
              ? "#f97316"
              : isSelectedNode
              ? "#4f46e5"
              : "#d6d3d1";

            const nodeStrokeWidth = isHighlightedNode || isSelectedNode ? 3 : 1.5;

            const x = node.x ?? 0;
            const y = node.y ?? 0;

            const isSource = sourceNode === node.id;
            const isTarget = targetNode === node.id;
            const isHighlighted = highlightedNodes.has(node.id);
            const isDragging = dragState?.nodeId === node.id;

            let gradient = "url(#nodeGradientDefault)";
            let textColor = "#57534e";
            let ringColor = "rgba(79,70,229,.22)";

            if (isSource) {
              gradient = "url(#nodeGradientSource)";
              textColor = "#ffffff";
            }

            if (isTarget) {
              gradient = "url(#nodeGradientTarget)";
              textColor = "#ffffff";
              ringColor = "rgba(21,128,61,.30)";
            }

            if (isSelectedNode) {
              gradient = "url(#nodeGradientHighlighted)";
              textColor = "#ffffff";
            }

            if (isHighlightedNode) {
              gradient = "url(#nodeGradientTarget)";
              textColor = "#ffffff";
            }

            const algorithmColor = getColorFromValue(nodeColors[node.id]);

            if (algorithmColor) {
              gradient = algorithmColor;
              textColor = "#ffffff";
              ringColor = algorithmColor;
            }

            const displayedLabel = nodeLabels[node.id] ?? node.label;

            const colorPalette = [
              "#4f46e5",
              "#16a34a",
              "#f97316",
              "#dc2626",
              "#0891b2",
              "#9333ea",
              "#ca8a04",
              "#0f766e",
            ];

            function getColorFromValue(value: unknown) {
              if (!value) return null;

              const str = String(value);

              if (str.startsWith("#") || str.startsWith("rgb")) {
                return str;
              }

              const match = str.match(/\d+/);
              const index = match ? Number(match[0]) - 1 : 0;

              return colorPalette[Math.abs(index) % colorPalette.length];
            }

            return (
              <g
                key={node.id}
                className={`graph-node-group ${
                  isHighlighted ? "is-active" : ""
                } ${isDragging ? "is-dragging" : ""}`}
                onPointerDown={(event) => {
                  event.stopPropagation();

                  const svg = event.currentTarget.ownerSVGElement;
                  if (!svg) return;

                  const svgPoint = svg.createSVGPoint();
                  svgPoint.x = event.clientX;
                  svgPoint.y = event.clientY;

                  const ctm = svg.getScreenCTM();
                  if (!ctm) return;

                  const point = svgPoint.matrixTransform(ctm.inverse());

                  setDragState({
                    nodeId: node.id,
                    offsetX: point.x - x,
                    offsetY: point.y - y,
                  });

                  event.currentTarget.setPointerCapture(event.pointerId);
                }}
              >
                <ellipse
                  className="graph-node-shadow"
                  cx={x}
                  cy={y + 18}
                  rx="18"
                  ry="7"
                />

                <circle
                  className={
                    isHighlightedNode
                      ? "graph-node-main node-current"
                      : isSelectedNode
                      ? "graph-node-main node-selected"
                      : "graph-node-main"
                  }
                  cx={x}
                  cy={y}
                  r="22"
                  fill={gradient}
                />

                <g className="graph-node-core">
                  <circle
                    className="graph-node-main"
                    cx={x}
                    cy={y}
                    r="22"
                    fill={gradient}
                  />

                  <circle
                    className="graph-node-highlight"
                    cx={x - 7}
                    cy={y - 7}
                    r="7"
                  />

                  <text
                    className="graph-node-label"
                    x={x}
                    y={y + 5}
                    textAnchor="middle"
                    fill={textColor}
                  >
                    {displayedLabel}
                  </text>
                </g>
              </g>
            );
          })}
        </svg>
      </div>

      <div className="graph-legend">
        <span className="legend-chip legend-source">● Source</span>
        <span className="legend-chip legend-target">
          ● {executionResult?.algorithm === "ford-fulkerson"
            ? "Puits"
            : "Destination"}
        </span>
        <span className="legend-chip legend-default">● Sommet normal</span>
        <span className="legend-chip legend-highlight">● Résultat</span>
      </div>
    </div>
  );
}