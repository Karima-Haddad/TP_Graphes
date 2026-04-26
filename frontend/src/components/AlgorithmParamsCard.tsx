import type { Graph } from "../types/graph.types";
import type { AlgorithmOption } from "../types/algorithm.types";

type Props = {
  graph: Graph;
  algorithm: AlgorithmOption;
  sourceNode: string;
  targetNode: string;
  displayMode: string;
  executionMode: string;
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
  onSourceChange,
  onTargetChange,
  onDisplayModeChange,
  onExecutionModeChange,
  onExecute,
  onNextStep,
  onPrevStep,
  onPlay,
  onPause,
  onResetSteps,
}: Props) {
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
            <label>Sommet destination</label>
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
          <label>Mode d’affichage</label>
          <select
            value={displayMode}
            onChange={(e) => onDisplayModeChange(e.target.value)}
            disabled={isLoading}
          >
            <option>Chemin complet + coût</option>
            <option>Distances seulement</option>
            <option>Tables détaillées</option>
          </select>
        </div>

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
          disabled={isLoading || !isCompatible}
        >
          {isLoading ? "Exécution..." : "▶ Exécuter"}
        </button>

        <button
          type="button"
          className="btn btn-ghost"
          onClick={onPrevStep}
          disabled={!stepControlsEnabled}
        >
          ← Étape précédente
        </button>

        <button
          type="button"
          className="btn btn-ghost"
          onClick={onNextStep}
          disabled={!stepControlsEnabled}
        >
          → Étape suivante
        </button>

        {!isPlaying ? (
          <button
            type="button"
            className="btn btn-ghost"
            onClick={onPlay}
            disabled={!stepControlsEnabled}
          >
            ▶ Lecture
          </button>
        ) : (
          <button
            type="button"
            className="btn btn-ghost"
            onClick={onPause}
          >
            ⏸ Pause
          </button>
        )}

        <button
          type="button"
          className="btn btn-ghost"
          onClick={onResetSteps}
          disabled={!stepControlsEnabled}
        >
          ↺ Réinitialiser
        </button>
      </div>

      {executionMode === "Directe" && (
        <div className="note">
          Le mode direct affiche immédiatement le résultat final sans navigation étape par étape.
        </div>
      )}

      {!isCompatible && (
        <div className="note" style={{ marginTop: "12px" }}>
          Cet algorithme ne peut pas être exécuté sur le graphe courant.
        </div>
      )}
    </div>
  );
}