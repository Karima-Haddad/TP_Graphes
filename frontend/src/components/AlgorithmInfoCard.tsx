import type { Graph } from "../types/graph.types";
import type { AlgorithmOption } from "../types/algorithm.types";
import type { CompatibilityResult } from "../utils/checkAlgorithmCompatibility";

type Props = {
  algorithm: AlgorithmOption;
  graph: Graph;
  compatibility: CompatibilityResult;
};

export function AlgorithmInfoCard({
  algorithm,
  compatibility,
}: Props) {
  return (
    <div className="card">
      <div className="card-title">Algorithme sélectionné</div>
      <div className="algo-name">{algorithm.label}</div>
      <p className="algo-desc">{algorithm.description}</p>

      <div className="side-list">
        {algorithm.requiresSource && (
          <div className="si info">Sommet source requis</div>
        )}

        {algorithm.requiresTarget && (
          <div className="si neutral">Sommet destination requis</div>
        )}

        <div className={`si ${compatibility.isCompatible ? "pass" : "neutral"}`}>
          {compatibility.message}
        </div>
      </div>
    </div>
  );
}