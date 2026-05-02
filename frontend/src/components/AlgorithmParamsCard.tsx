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
  executionMode,
  isLoading,
  isPlaying,
  stepControlsEnabled,
  isCompatible,
  executionFinished,
  onSourceChange,
  onTargetChange,
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
          {isStepMode ? (
            <>
              <svg className="btn-icon" viewBox="0 0 24 24" fill="none">
                <path d="M8 5v14l11-7L8 5Z" fill="currentColor" />
              </svg>
              Lire les étapes
            </>
          ) : (
            <>
              <svg className="btn-icon" viewBox="0 0 24 24" fill="none">
                <path d="M13 2L4 14h7l-1 8 10-13h-7l1-7Z" fill="currentColor" />
              </svg>
              Lancer l’algorithme
            </>
          )}
        </button>

        <button
          type="button"
          className="btn btn-ghost btn-icon-only"
          onClick={onPrevStep}
          disabled={!stepControlsEnabled || executionFinished}
        >
          <svg className="btn-icon" viewBox="0 0 24 24" fill="none">
            <path
              d="M15 6L9 12L15 18"
              stroke="currentColor"
              strokeWidth="2.4"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>

        <button
          type="button"
          className="btn btn-ghost btn-icon-only"
          onClick={onNextStep}
          disabled={!stepControlsEnabled || executionFinished}
        >
          <svg className="btn-icon" viewBox="0 0 24 24" fill="none">
            <path
              d="M9 6L15 12L9 18"
              stroke="currentColor"
              strokeWidth="2.4"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>

        <button
          type="button"
          className="btn btn-ghost btn-icon-only"
          onClick={onPause}
          disabled={!isPlaying || executionFinished}
        >
          <svg className="btn-icon" viewBox="0 0 24 24" fill="none">
            <path
              d="M8 5V19"
              stroke="currentColor"
              strokeWidth="2.6"
              strokeLinecap="round"
            />
            <path
              d="M16 5V19"
              stroke="currentColor"
              strokeWidth="2.6"
              strokeLinecap="round"
            />
          </svg>
        </button>

        <button
          type="button"
          className="btn btn-ghost btn-reset btn-icon-only"
          onClick={onResetSteps}
          disabled={isLoading}
        >
          <svg className="btn-icon" viewBox="0 0 24 24" fill="none">
            <path
              d="M4 12A8 8 0 1 0 6.35 6.35"
              stroke="currentColor"
              strokeWidth="2.2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M4 4V9H9"
              stroke="currentColor"
              strokeWidth="2.2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
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