import type { Graph } from "../types/graph.types";
import type { AlgorithmOption } from "../types/algorithm.types";

type Props = {
  graph: Graph;
  algorithm: AlgorithmOption;
  sourceNode: string;
  targetNode: string;
  displayMode: string;
  executionMode: string;
  executionFinished: boolean;
  onSourceChange: (value: string) => void;
  onTargetChange: (value: string) => void;
  onDisplayModeChange: (value: string) => void;
  onExecutionModeChange: (value: string) => void;
  onExecute: () => void;
  onNextStep: () => void;
  onPrevStep: () => void;
  onPlay: () => void;
  onPause: () => void;
  onResetSteps: () => void;
  isLoading: boolean;
  isPlaying: boolean;
  stepControlsEnabled: boolean;
  isCompatible: boolean;
};

export function AlgorithmParamsCard({
  graph,
  algorithm,
  sourceNode,
  targetNode,
  displayMode,
  executionMode,
  isLoading,
  isPlaying,
  stepControlsEnabled,
  isCompatible,
  executionFinished,
  onSourceChange,
  onTargetChange,
  onDisplayModeChange,
  onExecutionModeChange,
  onExecute,
  onNextStep,
  onPrevStep,
  onPause,
  onResetSteps,
}: Props) {
  const isStepMode = executionMode === "Pas à pas";
  const isFordFulkerson = algorithm.key === "ford-fulkerson";

  return (
    <div className="card">
      <div className="card-title">Paramètres d’exécution</div>

      <div className="form-row">
        {algorithm.requiresSource && (
          <div className="field">
            <label>Sommet source</label>
            <select
              value={sourceNode}
              onChange={(e) => onSourceChange(e.target.value)}
              disabled={isLoading}
            >
              {graph.nodes.map((node) => (
                <option key={node.id} value={node.id}>
                  {node.label}
                </option>
              ))}
            </select>
          </div>
        )}

        {algorithm.requiresTarget && (
          <div className="field">
            <label>{isFordFulkerson ? "Puits" : "Sommet destination"}</label>
            <select
              value={targetNode}
              onChange={(e) => onTargetChange(e.target.value)}
              disabled={isLoading}
            >
              {graph.nodes.map((node) => (
                <option key={node.id} value={node.id}>
                  {node.label}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      <div className="form-row">
        

        <div className="field">
          <label>Exécution</label>
          <select
            value={executionMode}
            onChange={(e) => onExecutionModeChange(e.target.value)}
            disabled={isLoading}
          >
            <option>Pas à pas</option>
            <option>Directe</option>
          </select>
        </div>
      </div>

      <div className="btn-row">
        <button
          type="button"
          className="btn btn-success"
          onClick={onExecute}
          disabled={isLoading || !isCompatible || executionFinished}
        >
          {isStepMode ? "▶ Lire les étapes" : "⚡ Lancer l’algorithme"}
        </button>

        <button
          type="button"
          className="btn btn-ghost"
          onClick={onPrevStep}
          disabled={!stepControlsEnabled || executionFinished}
        >
          ← Étape précédente
        </button>

        <button
          type="button"
          className="btn btn-ghost"
          onClick={onNextStep}
          disabled={!stepControlsEnabled || executionFinished}
        >
          → Étape suivante
        </button>

        <button
          type="button"
          className="btn btn-ghost"
          onClick={onPause}
          disabled={!isPlaying || executionFinished}
        >
          ⏸ Pause
        </button>

        <button
          type="button"
          className="btn btn-ghost btn-reset"
          onClick={onResetSteps}
          disabled={isLoading}
        >
          ↺ Réinitialiser
        </button>
      </div>

      {executionMode === "Directe" && (
        <div className="note note-direct">
          Le mode direct affiche immédiatement le résultat final sans navigation
          étape par étape.
        </div>
      )}

      {!isCompatible && (
        <div className="note note-error" style={{ marginTop: "12px" }}>
          Cet algorithme ne peut pas être exécuté sur le graphe courant.
        </div>
      )}
    </div>
  );
}