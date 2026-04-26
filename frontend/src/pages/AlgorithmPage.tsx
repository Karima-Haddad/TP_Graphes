import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import type { Graph } from "../types/graph.types";
import type { AlgorithmKey } from "../types/algorithm.types";
import { ALGORITHMS } from "../data/algorithms";
import { buildExecutionRequest } from "../utils/buildExecutionRequest";
import { AlgorithmSidebar } from "../components/AlgorithmSidebar";
import { AlgorithmInfoCard } from "../components/AlgorithmInfoCard";
import { AlgorithmParamsCard } from "../components/AlgorithmParamsCard";
import { AlgorithmResultCard } from "../components/AlgorithmResultCard";
import { AlgorithmVisualizationCard } from "../components/AlgorithmVisualizationCard";
import { executeAlgorithm } from "../services/executionApi";
import type { ExecutionResponse } from "../types/executionResponse.types";
import { checkAlgorithmCompatibility } from "../utils/checkAlgorithmCompatibility";
import "../styles/algorithm-page.css";

const fallbackGraph: Graph = {
  directed: false,
  weighted: true,
  nodes: [
    { id: "A", label: "A", x: 120, y: 80 },
    { id: "B", label: "B", x: 300, y: 125 },
    { id: "C", label: "C", x: 115, y: 215 },
    { id: "D", label: "D", x: 320, y: 245 },
    { id: "E", label: "E", x: 450, y: 190 },
  ],
  edges: [
    { id: "e1", source: "A", target: "B", weight: 4, label: "4" },
    { id: "e2", source: "A", target: "C", weight: 2, label: "2" },
    { id: "e3", source: "B", target: "D", weight: 5, label: "5" },
    { id: "e4", source: "C", target: "D", weight: 1, label: "1" },
    { id: "e5", source: "D", target: "E", weight: 3, label: "3" },
  ],
};




export default function AlgorithmPage() {
  const navigate = useNavigate();

  function getStoredGraph(): Graph | null {
    const saved = localStorage.getItem("graphData");

    if (!saved) return null;

    try {
      return JSON.parse(saved) as Graph;
    } catch {
      return null;
    }
  }

  const graph = useMemo(() => {
    return getStoredGraph() ?? fallbackGraph;
  }, []);

  
  const [selectedAlgorithm, setSelectedAlgorithm] =
    useState<AlgorithmKey>("dijkstra");
  const [sourceNode, setSourceNode] = useState(graph.nodes[0]?.id ?? "");
  const [targetNode, setTargetNode] = useState(graph.nodes[graph.nodes.length - 1]?.id ?? "");
  const [displayMode, setDisplayMode] = useState("Chemin complet + coût");
  const [executionMode, setExecutionMode] = useState("Pas à pas");

  const [executionResult, setExecutionResult] = useState<ExecutionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isStepMode, setIsStepMode] = useState(true);
  const [isPlaying, setIsPlaying] = useState(false);

  const selectedAlgo = useMemo(
    () => ALGORITHMS.find((algo) => algo.key === selectedAlgorithm)!,
    [selectedAlgorithm]
  );


  const compatibility = useMemo(() => {
    return checkAlgorithmCompatibility(graph, selectedAlgo);
  }, [graph, selectedAlgo]);

  const currentStep =
    executionResult &&
    executionResult.success &&
    isStepMode &&
    executionResult.visualization.steps.length > 0
      ? executionResult.visualization.steps[currentStepIndex]
      : null;

  
  const totalSteps =
    executionResult && executionResult.success
      ? executionResult.visualization.steps.length
      : 0;

  const stepControlsEnabled = executionMode === "Pas à pas" && totalSteps > 0;

  const handleNextStep = () => {
    if (
      !executionResult ||
      !executionResult.success ||
      executionResult.visualization.steps.length === 0
    ) {
      return;
    }

    setCurrentStepIndex((prev) =>
      Math.min(prev + 1, executionResult.visualization.steps.length - 1)
    );
  };

  const handlePrevStep = () => {
    setCurrentStepIndex((prev) => Math.max(prev - 1, 0));
  };

  const handleResetSteps = () => {
    setCurrentStepIndex(0);
    setIsPlaying(false);
  };

  const handlePlay = () => {
    if (!executionResult || !executionResult.success || totalSteps === 0) return;
    setIsStepMode(true);
    setIsPlaying(true);
  };

  const handlePause = () => {
    setIsPlaying(false);
  };

  const handleExecute = async () => {
    if (!compatibility.isCompatible) {
      setApiError("Exécution impossible : algorithme incompatible avec le graphe.");
      return;
    }
    try {
      setIsLoading(true);
      setApiError(null);

      const request = buildExecutionRequest({
          algorithm: selectedAlgorithm,
          graph,
          sourceNode,
          targetNode,
        });

        console.log("Execution request:", request);

        const response = await executeAlgorithm(request);

        console.log("Execution response:", response);

        setExecutionResult(response);
        setCurrentStepIndex(0);
        setIsPlaying(false);
        setIsStepMode(executionMode === "Pas à pas");
      } catch (error) {
        console.error(error);

        setApiError(
          error instanceof Error
            ? error.message
            : "Une erreur inconnue est survenue"
        );
      } finally {
        setIsLoading(false);
      }
    };


    useEffect(() => {
      if (!isPlaying) return;

      if (
        !executionResult ||
        !executionResult.success ||
        executionResult.visualization.steps.length === 0
      ) {
        return;
      }

      if (currentStepIndex >= executionResult.visualization.steps.length - 1) {
        setIsPlaying(false);
        return;
      }

      const timer = window.setTimeout(() => {
        setCurrentStepIndex((prev) => prev + 1);
      }, 1200);

      return () => window.clearTimeout(timer);
    }, [isPlaying, currentStepIndex, executionResult]);

  return (
    <div className="algorithm-page">
      <header className="topbar">
        <div className="logo">
          <div className="logo-mark">
            <svg viewBox="0 0 18 18" fill="none" aria-hidden="true">
              <circle cx="3.5" cy="3.5" r="2.5" fill="white" />
              <circle cx="14.5" cy="3.5" r="2.5" fill="white" />
              <circle cx="9" cy="14.5" r="2.5" fill="white" />
              <line x1="5.8" y1="3.5" x2="12.2" y2="3.5" stroke="white" strokeWidth="1.3" />
              <line x1="4.5" y1="5.5" x2="8" y2="12.5" stroke="white" strokeWidth="1.3" />
              <line x1="13.5" y1="5.5" x2="10" y2="12.5" stroke="white" strokeWidth="1.3" />
            </svg>
          </div>
          Graph<span>Lab</span>
        </div>

        {/* <div className="topbar-nav">
          <span className="nav-tab done">1. Graphe prêt</span>
          <span className="nav-tab active">2. Algorithme & résultat</span>
        </div> */}


        <div className="topbar-nav">
          <button
            type="button"
            className="nav-tab done"
            onClick={() => navigate("/")}
          >
            1. Graphe prêt
          </button>

          <button
            type="button"
            className="nav-tab active"
            disabled
          >
            2. Algorithme & résultat
          </button>
        </div>

      </header>

      <div className="layout">
        <AlgorithmSidebar
          algorithms={ALGORITHMS}
          selectedAlgorithm={selectedAlgorithm}
          onSelect={setSelectedAlgorithm}
        />

        <main className="main">
          <section className="page-header">
            <div className="page-eyebrow">Page 02</div>
            <h1 className="page-title">Choix de l’algorithme et résultat</h1>
            <p className="page-desc">
              Cette page regroupe la sélection de l’algorithme, la saisie des paramètres
              d’exécution et l’affichage détaillé du résultat obtenu.
            </p>
          </section>


          {apiError && (
            <div
              className="card"
              style={{
                marginBottom:"20px",
                borderColor:"#fecdd3",
                background:"#fff1f2"
              }}
            >
              <div className="card-title">
                Erreur d’exécution
              </div>

              <p>
                Une erreur est survenue lors de l’exécution.
                Veuillez réessayer.
              </p>

            </div>
          )}


          {executionResult && (
            <div
              className="card"
              style={{marginBottom:"20px"}}
            >
              <div className="card-title">
                Réponse brute backend
              </div>

              <pre>
                {JSON.stringify(
                  executionResult,
                  null,
                  2
                )}
              </pre>
            </div>
          )}


          {currentStep && (
            <div className="card" style={{ marginBottom: "20px" }}>
              <div className="card-title">
                Étape courante
              </div>

              <div className="result-block">
                <div className="r-label">Titre</div>
                <div className="r-value">{currentStep.title}</div>
              </div>

              <div className="result-block">
                <div className="r-label">Description</div>
                <div className="r-value">
                  {currentStep.description}
                </div>
              </div>

              <div className="result-block">
                <div className="r-label">Progression</div>

                <div className="r-value">
                  Étape {currentStepIndex + 1} /{" "}
                  {executionResult?.success
                    ? executionResult.visualization.steps.length
                    : 0}
                </div>
              </div>


              {/* AJOUTER ICI */}
              {executionResult?.success &&
                executionResult.visualization.steps.length > 0 && (
                <div style={{ marginTop:"12px" }}>
                  <div className="step-bar">
                    {executionResult.visualization.steps.map(
                      (_, index) => (
                        <div
                          key={index}
                          className={`step-dot ${
                            index <= currentStepIndex
                              ? "done"
                              : ""
                          }`}
                        />
                      )
                    )}
                  </div>
                </div>
              )}

            </div>
          )}

          <section className="grid grid-2">
            <div className="col">
              <AlgorithmInfoCard
                algorithm={selectedAlgo}
                graph={graph}
                compatibility={compatibility}
              />

              <AlgorithmParamsCard
                graph={graph}
                algorithm={selectedAlgo}
                sourceNode={sourceNode}
                targetNode={targetNode}
                displayMode={displayMode}
                executionMode={executionMode}
                onSourceChange={setSourceNode}
                onTargetChange={setTargetNode}
                onDisplayModeChange={setDisplayMode}
                onExecutionModeChange={setExecutionMode}
                onExecute={handleExecute}
                onNextStep={handleNextStep}
                onPrevStep={handlePrevStep}
                onPlay={handlePlay}
                onPause={handlePause}
                onResetSteps={handleResetSteps}
                isLoading={isLoading}
                isPlaying={isPlaying}
                stepControlsEnabled={stepControlsEnabled}
                isCompatible={compatibility.isCompatible}
              />
            </div>

            <div className="col">
              <AlgorithmResultCard
                executionResult={executionResult}
                isLoading={isLoading}
              />
              <AlgorithmVisualizationCard
                graph={graph}
                executionResult={executionResult}
                currentStep={currentStep}
                sourceNode={sourceNode}
                targetNode={targetNode}
              />
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}