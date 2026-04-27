import React, { useRef, useEffect, useState } from 'react';
import type { Graph, GraphNode } from '../types/graph.types';
import '../styles/VisualisationGraphe.css';

interface PropsVisualisationGraphe {
  graph: Graph | null;
  onGraphChange?: (graph: Graph) => void;
}

interface NodePosition {
  x: number;
  y: number;
  vx: number;
  vy: number;
  fixed: boolean;
}

export const VisualisationGraphe: React.FC<PropsVisualisationGraphe> = ({ graph }) => {
export const VisualisationGraphe: React.FC<PropsVisualisationGraphe> = ({ graph, onGraphChange }) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const positionsRef = useRef<Map<string, NodePosition>>(new Map());
  const [positions, setPositions] = useState<Map<string, NodePosition>>(new Map());
  const [dragging, setDragging] = useState<string | null>(null);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const animationRef = useRef<number | null>(null);
  const isRunningRef = useRef(false);

  // Initialiser les positions quand le graph change
  useEffect(() => {
    if (!graph) return;

    isRunningRef.current = false;
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
      animationRef.current = null;
    }

    setDragging(null);
    setDragOffset({ x: 0, y: 0 });

    const initialPositions = new Map<string, NodePosition>();
    const centerX = 400;
    const centerY = 195;
    const radius = 140;

    graph.nodes.forEach((node, index) => {
      const angle = (index * 2 * Math.PI) / graph.nodes.length - Math.PI / 2;
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);

      initialPositions.set(node.id, {
        x,
        y,
        vx: 0,
        vy: 0,
        fixed: false,
      });
    });

    positionsRef.current = initialPositions;
    setPositions(new Map(initialPositions));

    isRunningRef.current = true;
    startSimulation(graph);
  }, [graph]);

  // Fonction de simulation
  const startSimulation = (currentGraph: Graph) => {
    const simulate = () => {
      if (!isRunningRef.current) return;

      positionsRef.current.forEach((nodePos, nodeId) => {
        if (nodePos.fixed) return;

        let fx = 0;
        let fy = 0;

        const k = 0.001; // ✅ RÉDUIT DE 100x
        const c = 0.95; // ✅ Moins d'amortissement
        const repulsion = 1000; // ✅ RÉDUIT DE 5x

        // Répulsion entre nœuds
        positionsRef.current.forEach((otherPos, otherId) => {
          if (nodeId === otherId) return;

          const dx = nodePos.x - otherPos.x;
          const dy = nodePos.y - otherPos.y;
          const dist = Math.sqrt(dx * dx + dy * dy) || 1;

          const force = repulsion / (dist * dist);
          fx += (dx / dist) * force;
          fy += (dy / dist) * force;
        });

        // Attraction vers les nœuds connectés - ✅ TRÈS FAIBLE
        currentGraph.edges.forEach((edge) => {
          if (edge.source === nodeId) {
            const other = positionsRef.current.get(edge.target);
            if (!other) return;

            const dx = other.x - nodePos.x;
            const dy = other.y - nodePos.y;
            const dist = Math.sqrt(dx * dx + dy * dy) || 1;

            const force = k * dist * 0.1; // ✅ Encore plus réduit
            fx += (dx / dist) * force;
            fy += (dy / dist) * force;
          } else if (edge.target === nodeId) {
            const other = positionsRef.current.get(edge.source);
            if (!other) return;

            const dx = other.x - nodePos.x;
            const dy = other.y - nodePos.y;
            const dist = Math.sqrt(dx * dx + dy * dy) || 1;

            const force = k * dist * 0.1; // ✅ Encore plus réduit
            fx += (dx / dist) * force;
            fy += (dy / dist) * force;
          }
        });

        // Appliquer les forces
        nodePos.vx = (nodePos.vx + fx) * c;
        nodePos.vy = (nodePos.vy + fy) * c;

        nodePos.x += nodePos.vx;
        nodePos.y += nodePos.vy;

        // Limiter dans la zone
        const padding = 40;
        nodePos.x = Math.max(padding, Math.min(790 - padding, nodePos.x));
        nodePos.y = Math.max(padding, Math.min(360 - padding, nodePos.y));
      });

      // Mettre à jour le state React
      setPositions(new Map(positionsRef.current));
      animationRef.current = requestAnimationFrame(simulate);
    };

    animationRef.current = requestAnimationFrame(simulate);
  };

  // Gestion du drag - Mouse Down
  const handleMouseDown = (e: React.MouseEvent<SVGCircleElement>, nodeId: string) => {
    e.preventDefault();
    e.stopPropagation();
    const svg = svgRef.current;
    if (!svg) return;

    const rect = svg.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const nodePos = positionsRef.current.get(nodeId);
    if (!nodePos) return;

    setDragOffset({
      x: x - nodePos.x,
      y: y - nodePos.y,
    });

    setDragging(nodeId);

    // ✅ Fixer SEULEMENT ce nœud et réinitialiser sa vitesse
    nodePos.fixed = true;
    nodePos.vx = 0;
    nodePos.vy = 0;
  };

  // Gestion du drag - Mouse Move
  const handleMouseMove = (e: React.MouseEvent<SVGSVGElement>) => {
    if (!dragging || !svgRef.current) return;

    const rect = svgRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const draggedX = x - dragOffset.x;
    const draggedY = y - dragOffset.y;

    // Limiter dans la zone
    const padding = 40;
    const boundedX = Math.max(padding, Math.min(790 - padding, draggedX));
    const boundedY = Math.max(padding, Math.min(360 - padding, draggedY));

    const pos = positionsRef.current.get(dragging);
    if (pos) {
      pos.x = boundedX;
      pos.y = boundedY;
      pos.vx = 0; // ✅ Réinitialiser la vitesse à chaque mouvement
      pos.vy = 0;
      setPositions(new Map(positionsRef.current));
    }
  };

  // Gestion du drag - Mouse Up
  const handleMouseUp = () => {
    if (dragging) {
      const pos = positionsRef.current.get(dragging);
      if (pos) {
        pos.fixed = false; // ✅ Libérer le nœud
        // Ne pas réinitialiser vx/vy pour laisser l'inertie
      }
      setDragging(null);
    }
  };

  useEffect(() => {
    window.addEventListener('mouseup', handleMouseUp);
    return () => {
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [dragging]);

  // Cleanup
  useEffect(() => {
    return () => {
      isRunningRef.current = false;
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []);

  // Fonctions utilitaires pour Bezier
  const pointSurBezier = (
    x0: number,
    y0: number,
    cx: number,
    cy: number,
    x1: number,
    y1: number,
    t: number
  ) => {
    const mt = 1 - t;
    const x = mt * mt * x0 + 2 * mt * t * cx + t * t * x1;
    const y = mt * mt * y0 + 2 * mt * t * cy + t * t * y1;
    return { x, y };
  };

  const tangenteBezier = (
    x0: number,
    y0: number,
    cx: number,
    cy: number,
    x1: number,
    y1: number,
    t: number
  ) => {
    const mt = 1 - t;
    const dx = 2 * mt * (cx - x0) + 2 * t * (x1 - cx);
    const dy = 2 * mt * (cy - y0) + 2 * t * (y1 - cy);
    const len = Math.sqrt(dx * dx + dy * dy) || 1;
    return { dx: dx / len, dy: dy / len };
  };

  // Dessiner le graphe
  useEffect(() => {
    if (!graph || !svgRef.current || positions.size === 0) return;

    const svg = svgRef.current;
    svg.innerHTML = '';

    const nodeRadius = 28;

    const updatedNodes = graph.nodes.map((node) => {
  const pos = positions.get(node.id);

  return {
    ...node,
    x: pos?.x ?? node.x,
    y: pos?.y ?? node.y,
  };
});

const positionsDifferent =
  graph.nodes.some((node, index) => {
    return (
      node.x !== updatedNodes[index].x ||
      node.y !== updatedNodes[index].y
    );
  });

if (positionsDifferent) {
  onGraphChange?.({
    ...graph,
    nodes: updatedNodes,
  });
}

    // Groupe pour les arêtes
    const edgesGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    edgesGroup.setAttribute('id', 'edges');

    const loopsGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    loopsGroup.setAttribute('id', 'loops');

    const labelsGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    labelsGroup.setAttribute('id', 'labels');

    const arrowsGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    arrowsGroup.setAttribute('id', 'arrows');

    const edgeMap = new Map<string, number>();

    // Dessiner les arêtes
    graph.edges.forEach((edge) => {
      const posSource = positions.get(edge.source);
      const posTarget = positions.get(edge.target);

      if (!posSource || !posTarget) return;

      // BOUCLE (A,A)
      if (edge.source === edge.target) {
        const loopRadius = 40;
        const loopCx = posSource.x + loopRadius;
        const loopCy = posSource.y - loopRadius;

        const chemin = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const pathData = `M ${posSource.x + nodeRadius} ${posSource.y} A ${loopRadius} ${loopRadius} 0 1 1 ${posSource.x + nodeRadius - 2} ${posSource.y}`;
        chemin.setAttribute('d', pathData);
        chemin.setAttribute('fill', 'none');
        chemin.setAttribute('stroke', '#4f46e5');
        chemin.setAttribute('stroke-width', '2.5');
        chemin.setAttribute('stroke-linecap', 'round');
        loopsGroup.appendChild(chemin);

        if (graph.directed) {
          const arrowSize = 11;
          const arrowAngle = -Math.PI / 4;

          const arrowX = loopCx + loopRadius * Math.cos(arrowAngle);
          const arrowY = loopCy + loopRadius * Math.sin(arrowAngle);

          const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
          const angle = arrowAngle + Math.PI / 2;
          const points = [
            [arrowX, arrowY],
            [
              arrowX - arrowSize * Math.cos(angle - Math.PI / 6),
              arrowY - arrowSize * Math.sin(angle - Math.PI / 6),
            ],
            [
              arrowX - arrowSize * Math.cos(angle + Math.PI / 6),
              arrowY - arrowSize * Math.sin(angle + Math.PI / 6),
            ],
          ];
          polygon.setAttribute(
            'points',
            points.map((p) => p.join(',')).join(' ')
          );
          polygon.setAttribute('fill', '#4f46e5');
          polygon.setAttribute('stroke', 'none');
          arrowsGroup.appendChild(polygon);
        }

        if (graph.weighted && edge.weight) {
          const labelX = loopCx + 25;
          const labelY = loopCy - 25;

          const bgRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
          bgRect.setAttribute('x', String(labelX - 18));
          bgRect.setAttribute('y', String(labelY - 14));
          bgRect.setAttribute('width', '36');
          bgRect.setAttribute('height', '28');
          bgRect.setAttribute('fill', '#ffffff');
          bgRect.setAttribute('stroke', '#4f46e5');
          bgRect.setAttribute('stroke-width', '2');
          bgRect.setAttribute('rx', '6');
          bgRect.setAttribute('filter', 'drop-shadow(0 2px 4px rgba(79, 70, 229, 0.15))');
          labelsGroup.appendChild(bgRect);

          const texte = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          texte.setAttribute('x', String(labelX));
          texte.setAttribute('y', String(labelY + 5));
          texte.setAttribute('font-size', '13');
          texte.setAttribute('font-weight', '700');
          texte.setAttribute('fill', '#4f46e5');
          texte.setAttribute('text-anchor', 'middle');
          texte.setAttribute('font-family', 'DM Mono');
          texte.textContent = String(edge.weight);
          labelsGroup.appendChild(texte);
        }

        return;
      }

      // ARÊTES NORMALES
      const edgeKey = graph.directed
        ? `${edge.source}->${edge.target}`
        : [edge.source, edge.target].sort().join('-');

      const parallelIndex = edgeMap.get(edgeKey) || 0;
      edgeMap.set(edgeKey, parallelIndex + 1);

      const dx = posTarget.x - posSource.x;
      const dy = posTarget.y - posSource.y;
      const dist = Math.sqrt(dx * dx + dy * dy);

      if (dist < 5) return;

      const midX = (posSource.x + posTarget.x) / 2;
      const midY = (posSource.y + posTarget.y) / 2;

      const perpX = -dy / dist;
      const perpY = dx / dist;

      const offset = parallelIndex > 0 ? 40 * parallelIndex : 20;
      const controlX = midX + perpX * offset;
      const controlY = midY + perpY * offset;

      const chemin = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      const pathData = `M ${posSource.x} ${posSource.y} Q ${controlX} ${controlY} ${posTarget.x} ${posTarget.y}`;
      chemin.setAttribute('d', pathData);
      chemin.setAttribute('fill', 'none');
      chemin.setAttribute('stroke', '#d4cfc8');
      chemin.setAttribute('stroke-width', '2.5');
      chemin.setAttribute('stroke-linecap', 'round');
      edgesGroup.appendChild(chemin);

      if (graph.weighted && edge.weight) {
        const labelPoint = pointSurBezier(
          posSource.x,
          posSource.y,
          controlX,
          controlY,
          posTarget.x,
          posTarget.y,
          0.5
        );

        const tangente = tangenteBezier(
          posSource.x,
          posSource.y,
          controlX,
          controlY,
          posTarget.x,
          posTarget.y,
          0.5
        );

        const labelOffsetDist = 22;
        const labelX = labelPoint.x - tangente.dy * labelOffsetDist;
        const labelY = labelPoint.y + tangente.dx * labelOffsetDist;

        const bgRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        bgRect.setAttribute('x', String(labelX - 18));
        bgRect.setAttribute('y', String(labelY - 14));
        bgRect.setAttribute('width', '36');
        bgRect.setAttribute('height', '28');
        bgRect.setAttribute('fill', '#ffffff');
        bgRect.setAttribute('stroke', '#4f46e5');
        bgRect.setAttribute('stroke-width', '2');
        bgRect.setAttribute('rx', '6');
        bgRect.setAttribute('filter', 'drop-shadow(0 2px 4px rgba(79, 70, 229, 0.15))');
        labelsGroup.appendChild(bgRect);

        const texte = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        texte.setAttribute('x', String(labelX));
        texte.setAttribute('y', String(labelY + 5));
        texte.setAttribute('font-size', '13');
        texte.setAttribute('font-weight', '700');
        texte.setAttribute('fill', '#4f46e5');
        texte.setAttribute('text-anchor', 'middle');
        texte.setAttribute('font-family', 'DM Mono');
        texte.textContent = String(edge.weight);
        labelsGroup.appendChild(texte);
      }

      if (graph.directed) {
        const t = 0.05;
        const pointFleche = pointSurBezier(
          posSource.x,
          posSource.y,
          controlX,
          controlY,
          posTarget.x,
          posTarget.y,
          t
        );

        const tangente = tangenteBezier(
          posSource.x,
          posSource.y,
          controlX,
          controlY,
          posTarget.x,
          posTarget.y,
          t
        );

        const offsetFromNode = nodeRadius + 12;
        const arrowX = pointFleche.x + tangente.dx * offsetFromNode;
        const arrowY = pointFleche.y + tangente.dy * offsetFromNode;

        const arrowAngle = Math.atan2(tangente.dy, tangente.dx);
        const arrowSize = 13;

        const p1 = { x: arrowX, y: arrowY };
        const p2 = {
          x: arrowX - Math.cos(arrowAngle + Math.PI / 6) * arrowSize,
          y: arrowY - Math.sin(arrowAngle + Math.PI / 6) * arrowSize,
        };
        const p3 = {
          x: arrowX - Math.cos(arrowAngle - Math.PI / 6) * arrowSize,
          y: arrowY - Math.sin(arrowAngle - Math.PI / 6) * arrowSize,
        };

        const fleche = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        fleche.setAttribute('points', `${p1.x},${p1.y} ${p2.x},${p2.y} ${p3.x},${p3.y}`);
        fleche.setAttribute('fill', '#4f46e5');
        fleche.setAttribute('stroke', '#4f46e5');
        fleche.setAttribute('stroke-width', '0.5');
        fleche.setAttribute('opacity', '0.95');
        arrowsGroup.appendChild(fleche);
      }
    });

    svg.appendChild(edgesGroup);
    svg.appendChild(loopsGroup);

    const nodesGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    nodesGroup.setAttribute('id', 'nodes');

    const sortedNodes = [...graph.nodes].sort((a, b) => {
      const posA = positions.get(a.id);
      const posB = positions.get(b.id);
      return (posA?.y || 0) - (posB?.y || 0);
    });

    sortedNodes.forEach((node) => {
      const pos = positions.get(node.id);
      if (!pos) return;

      const ombre = document.createElementNS('http://www.w3.org/2000/svg', 'ellipse');
      ombre.setAttribute('cx', String(pos.x + 4));
      ombre.setAttribute('cy', String(pos.y + 32));
      ombre.setAttribute('rx', String(nodeRadius - 2));
      ombre.setAttribute('ry', String((nodeRadius - 2) * 0.3));
      ombre.setAttribute('fill', 'rgba(28, 25, 23, 0.1)');
      ombre.setAttribute('filter', 'blur(2px)');
      nodesGroup.appendChild(ombre);

      const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
      const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'radialGradient');
      gradient.setAttribute('id', `grad-${node.id}`);
      gradient.setAttribute('cx', '35%');
      gradient.setAttribute('cy', '35%');

      const stop1 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
      stop1.setAttribute('offset', '0%');
      stop1.setAttribute('stop-color', '#e0e7ff');

      const stop2 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
      stop2.setAttribute('offset', '100%');
      stop2.setAttribute('stop-color', '#c7d2fe');

      gradient.appendChild(stop1);
      gradient.appendChild(stop2);
      defs.appendChild(gradient);
      nodesGroup.appendChild(defs);

      const cercle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      cercle.setAttribute('cx', String(pos.x));
      cercle.setAttribute('cy', String(pos.y));
      cercle.setAttribute('r', String(nodeRadius));
      cercle.setAttribute('fill', `url(#grad-${node.id})`);
      cercle.setAttribute('stroke', '#4f46e5');
      cercle.setAttribute('stroke-width', '3');
      cercle.setAttribute('class', 'node-circle');
      cercle.setAttribute(
        'style',
        dragging === node.id
          ? 'cursor: grabbing; filter: drop-shadow(0 8px 16px rgba(79, 70, 229, 0.4))'
          : 'cursor: grab; transition: all 0.2s ease;'
      );
      cercle.addEventListener('mousedown', (e) => handleMouseDown(e as any, node.id));
      nodesGroup.appendChild(cercle);

      const highlight = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      highlight.setAttribute('cx', String(pos.x - 8));
      highlight.setAttribute('cy', String(pos.y - 8));
      highlight.setAttribute('r', String(nodeRadius * 0.4));
      highlight.setAttribute('fill', '#ffffff');
      highlight.setAttribute('opacity', '0.4');
      nodesGroup.appendChild(highlight);

      const texte = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      texte.setAttribute('x', String(pos.x));
      texte.setAttribute('y', String(pos.y + 6));
      texte.setAttribute('text-anchor', 'middle');
      texte.setAttribute('font-size', '16');
      texte.setAttribute('font-weight', '700');
      texte.setAttribute('fill', '#4f46e5');
      texte.setAttribute('font-family', 'DM Mono');
      texte.setAttribute('pointer-events', 'none');
      texte.setAttribute('user-select', 'none');
      texte.textContent = node.label;
      nodesGroup.appendChild(texte);
    });

    svg.appendChild(nodesGroup);
    svg.appendChild(labelsGroup);
    svg.appendChild(arrowsGroup);
  }, [positions, graph, dragging]);

  return (
    <div className="visualisation-graphe">
      <div className="card">
        <div className="card-title">Visualisation du graphe</div>
        <div className="visual-zone">
          <svg
            ref={svgRef}
            className="graph-svg"
            viewBox="0 0 800 390"
            onMouseMove={handleMouseMove}
            onMouseLeave={handleMouseUp}
          ></svg>
        </div>
        <div className="visualization-hint">
          💡 Glissez les nœuds pour les déplacer librement
        </div>
      </div>
    </div>
  );
};