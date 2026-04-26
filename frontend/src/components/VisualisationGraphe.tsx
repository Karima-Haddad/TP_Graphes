import React, { useRef, useEffect } from 'react';
import type { Graph, GraphNode } from '../types/graph.types';
import '../styles/VisualisationGraphe.css';

interface PropsVisualisationGraphe {
  graph: Graph | null;
}

export const VisualisationGraphe: React.FC<PropsVisualisationGraphe> = ({ graph }) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (graph && svgRef.current) {
      dessinerGraphe();
    }
  }, [graph]);

  const calculerPositions = (nodes: GraphNode[]) => {
    const centerX = 360;
    const centerY = 195;
    const radius = 140;
    const count = nodes.length;

    const positions = new Map<string, { x: number; y: number }>();

    nodes.forEach((node, index) => {
      const angle = (index * 2 * Math.PI) / count - Math.PI / 2;
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);

      positions.set(node.id, { x, y });
    });

    return positions;
  };

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
    const len = Math.sqrt(dx * dx + dy * dy);
    return { dx: dx / len, dy: dy / len };
  };

  const dessinerGraphe = () => {
    if (!graph || !svgRef.current) return;

    const svg = svgRef.current;
    svg.innerHTML = '';

    const positions = calculerPositions(graph.nodes);
    const nodeRadius = 28;

    // Groupe pour les arêtes
    const edgesGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    edgesGroup.setAttribute('id', 'edges');

    // Groupe pour les flèches
    const arrowsGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    arrowsGroup.setAttribute('id', 'arrows');

    // Groupe pour les boucles
    const loopsGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    loopsGroup.setAttribute('id', 'loops');

    // Map pour tracker les arêtes parallèles
    const edgeMap = new Map<string, number>();

    // Dessiner les arêtes et boucles
    graph.edges.forEach((edge) => {
      const posSource = positions.get(edge.source);
      const posTarget = positions.get(edge.target);

      if (!posSource || !posTarget) return;

      // BOUCLE (A,A)
      if (edge.source === edge.target) {
        const loopRadius = 35;
        const loopCx = posSource.x + loopRadius;
        const loopCy = posSource.y - loopRadius;

        // Chemin de la boucle (cercle)
        const chemin = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const pathData = `M ${posSource.x + nodeRadius} ${posSource.y} A ${loopRadius} ${loopRadius} 0 1 1 ${posSource.x + nodeRadius - 2} ${posSource.y}`;
        chemin.setAttribute('d', pathData);
        chemin.setAttribute('fill', 'none');
        chemin.setAttribute('stroke', '#4f46e5');
        chemin.setAttribute('stroke-width', '2.5');
        chemin.setAttribute('stroke-linecap', 'round');
        loopsGroup.appendChild(chemin);

        // Flèche pour boucle orientée
        if (graph.directed) {
          const arrowSize = 10;
          const arrowAngle = -Math.PI / 4; // Angle en haut à droite

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

        // Poids pour boucle pondérée
        if (graph.weighted && edge.weight) {
          const labelX = loopCx + 15;
          const labelY = loopCy - 15;

          const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
          rect.setAttribute('x', String(labelX - 16));
          rect.setAttribute('y', String(labelY - 11));
          rect.setAttribute('width', '32');
          rect.setAttribute('height', '22');
          rect.setAttribute('fill', '#ffffff');
          rect.setAttribute('stroke', '#4f46e5');
          rect.setAttribute('stroke-width', '1.5');
          rect.setAttribute('rx', '4');
          loopsGroup.appendChild(rect);

          const texte = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          texte.setAttribute('x', String(labelX));
          texte.setAttribute('y', String(labelY + 5));
          texte.setAttribute('font-size', '12');
          texte.setAttribute('font-weight', '700');
          texte.setAttribute('fill', '#4f46e5');
          texte.setAttribute('text-anchor', 'middle');
          texte.setAttribute('font-family', 'DM Mono');
          texte.textContent = String(edge.weight);
          loopsGroup.appendChild(texte);
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

      const offset = parallelIndex > 0 ? 30 * parallelIndex : 15;
      const controlX = midX + perpX * offset;
      const controlY = midY + perpY * offset;

      // Chemin courbe
      const chemin = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      const pathData = `M ${posSource.x} ${posSource.y} Q ${controlX} ${controlY} ${posTarget.x} ${posTarget.y}`;
      chemin.setAttribute('d', pathData);
      chemin.setAttribute('fill', 'none');
      chemin.setAttribute('stroke', '#4f46e5');
      chemin.setAttribute('stroke-width', '2.5');
      chemin.setAttribute('stroke-linecap', 'round');
      edgesGroup.appendChild(chemin);

      // Flèche orientée
      if (graph.directed) {
        const pointFleche = pointSurBezier(
          posSource.x,
          posSource.y,
          controlX,
          controlY,
          posTarget.x,
          posTarget.y,
          0.8
        );

        const tangente = tangenteBezier(
          posSource.x,
          posSource.y,
          controlX,
          controlY,
          posTarget.x,
          posTarget.y,
          0.8
        );

        const tailleFleche = 10;
        const anglePerp = Math.atan2(tangente.dy, tangente.dx);

        const p1 = {
          x: pointFleche.x + tangente.dx * tailleFleche,
          y: pointFleche.y + tangente.dy * tailleFleche,
        };

        const p2 = {
          x: pointFleche.x - Math.sin(anglePerp) * (tailleFleche * 0.7),
          y: pointFleche.y + Math.cos(anglePerp) * (tailleFleche * 0.7),
        };

        const p3 = {
          x: pointFleche.x + Math.sin(anglePerp) * (tailleFleche * 0.7),
          y: pointFleche.y - Math.cos(anglePerp) * (tailleFleche * 0.7),
        };

        const fleche = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        fleche.setAttribute('points', `${p1.x},${p1.y} ${p2.x},${p2.y} ${p3.x},${p3.y}`);
        fleche.setAttribute('fill', '#4f46e5');
        fleche.setAttribute('stroke', 'none');
        arrowsGroup.appendChild(fleche);
      }

      // Poids
      if (graph.weighted && edge.weight) {
        const labelX = controlX;
        const labelY = controlY - 14;

        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', String(labelX - 16));
        rect.setAttribute('y', String(labelY - 11));
        rect.setAttribute('width', '32');
        rect.setAttribute('height', '22');
        rect.setAttribute('fill', '#ffffff');
        rect.setAttribute('stroke', '#4f46e5');
        rect.setAttribute('stroke-width', '1.5');
        rect.setAttribute('rx', '4');
        edgesGroup.appendChild(rect);

        const texte = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        texte.setAttribute('x', String(labelX));
        texte.setAttribute('y', String(labelY + 5));
        texte.setAttribute('font-size', '12');
        texte.setAttribute('font-weight', '700');
        texte.setAttribute('fill', '#4f46e5');
        texte.setAttribute('text-anchor', 'middle');
        texte.setAttribute('font-family', 'DM Mono');
        texte.textContent = String(edge.weight);
        edgesGroup.appendChild(texte);
      }
    });

    svg.appendChild(edgesGroup);
    svg.appendChild(loopsGroup);
    svg.appendChild(arrowsGroup);

    // Groupe pour les nœuds
    const nodesGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    nodesGroup.setAttribute('id', 'nodes');

    // Dessiner les nœuds
    graph.nodes.forEach((node) => {
      const pos = positions.get(node.id);
      if (!pos) return;

      const cercle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      cercle.setAttribute('cx', String(pos.x));
      cercle.setAttribute('cy', String(pos.y));
      cercle.setAttribute('r', String(nodeRadius));
      cercle.setAttribute('fill', '#eef2ff');
      cercle.setAttribute('stroke', '#4f46e5');
      cercle.setAttribute('stroke-width', '3');
      cercle.setAttribute('class', 'node-circle');
      nodesGroup.appendChild(cercle);

      const texte = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      texte.setAttribute('x', String(pos.x));
      texte.setAttribute('y', String(pos.y + 6));
      texte.setAttribute('text-anchor', 'middle');
      texte.setAttribute('font-size', '16');
      texte.setAttribute('font-weight', '700');
      texte.setAttribute('fill', '#4f46e5');
      texte.setAttribute('font-family', 'DM Mono');
      texte.textContent = node.label;
      texte.setAttribute('pointer-events', 'none');
      nodesGroup.appendChild(texte);
    });

    svg.appendChild(nodesGroup);
  };

  return (
    <div className="visualisation-graphe">
      <div className="card">
        <div className="card-title">Visualisation du graphe</div>
        <div className="visual-zone">
          <svg ref={svgRef} className="graph-svg" viewBox="0 0 720 390"></svg>
        </div>
      </div>
    </div>
  );
};