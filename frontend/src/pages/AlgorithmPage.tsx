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
import { fetchGraphProperties } from "../services/executionApi";
import { fetchConnectedComponents } from "../services/executionApi";
import { useRef } from "react";
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
  const [graphProperties, setGraphProperties] = useState<any>(null);
  const resultRef = useRef<HTMLDivElement | null>(null);

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

    useEffect(() => {
    async function loadGraphProperties() {
      if (selectedAlgorithm !== "prim") {
        setGraphProperties(null);
        return;
      }

      try {
        const data = await fetchConnectedComponents(graph);
        setGraphProperties(data);
      } catch (error) {
        console.error(error);
        setGraphProperties(null);
      }
    }

    loadGraphProperties();
  }, [selectedAlgorithm, graph]);


  const compatibility = useMemo(() => {
    return checkAlgorithmCompatibility(graph, selectedAlgo, graphProperties);
  }, [graph, selectedAlgo, graphProperties]);

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

  const executionFinished =
  executionResult?.success === true &&
  (
    executionMode !== "Pas à pas" ||
    currentStepIndex === totalSteps - 1
  );

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
    setIsPlaying(false);

    setCurrentStepIndex(0);

    setExecutionResult(null);

    setIsStepMode(false);
  };

  const handlePlay = async () => {

    if(!executionResult){
    await handleExecute();
    }

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

    const stepsLength =
      response.success ? response.visualization.steps.length : 0;

    if (executionMode === "Pas à pas") {
      setCurrentStepIndex(0);
      setIsStepMode(true);
      setIsPlaying(false);
    } else {
      setCurrentStepIndex(Math.max(stepsLength - 1, 0));
      setIsStepMode(false);
      setIsPlaying(false);
    }

    } catch (error) {
      console.error(error);

      setApiError(
        error instanceof Error
          ? error.message
          : "Une erreur inconnue est survenue"
      );

      setIsPlaying(false);
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

    const summary = (executionResult?.result?.summary as any) || {};
    const details = (executionResult?.result?.details as any) || {};

    useEffect(() => {
      setExecutionResult(null);
      setCurrentStepIndex(0);
      setIsPlaying(false);
    }, [selectedAlgorithm]);


    useEffect(() => {
      async function loadProperties() {
        try {
          const props = await fetchGraphProperties(graph);
          console.log("Graph properties:", props);
          setGraphProperties(props);
        } catch (error) {
          console.error(error);
        }
      }

      loadProperties();
    }, [graph]);

    useEffect(() => {
      if (executionResult?.success === false && resultRef.current) {
        resultRef.current.scrollIntoView({
          behavior: "smooth",
          block: "center"
        });
      }
    }, [executionResult]);
    
  return (
      <div className="algorithm-page">

      <header className="topbar">

      <div className="logo">
      <div className="logo-mark">
      <svg viewBox="0 0 18 18" fill="none">
      <circle cx="3.5" cy="3.5" r="2.5" fill="white"/>
      <circle cx="14.5" cy="3.5" r="2.5" fill="white"/>
      <circle cx="9" cy="14.5" r="2.5" fill="white"/>
      <line x1="5.8" y1="3.5" x2="12.2" y2="3.5" stroke="white"/>
      <line x1="4.5" y1="5.5" x2="8" y2="12.5" stroke="white"/>
      <line x1="13.5" y1="5.5" x2="10" y2="12.5" stroke="white"/>
      </svg>
      </div>

      Graph<span>Lab</span>

      </div>


      <div className="topbar-nav">

      <button
      type="button"
      className="nav-tab done"
      onClick={()=>navigate("/")}
      >
      1. Graphe prêt
      </button>

      <button
      type="button"
      className="nav-tab active"
      disabled
      >
      2. Algorithmes & résultats
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

      {/* <div className="page-eyebrow">
      Page 02
      </div> */}

      <h1 className="page-title">
      Simulation d’algorithmes
      </h1>

      <p className="page-desc">
      Configurer, exécuter puis explorer pas à pas.
      </p>

      </section>


      {apiError && (
      <div className="card">
      <div className="result-block highlight">
      <div className="r-label">
      Erreur
      </div>

      <div className="r-value">
      {apiError}
      </div>

      </div>
      </div>
      )}



      <section className="page-content-fixed">

        <div className="info-full">
          <AlgorithmInfoCard
            algorithm={selectedAlgo}
            graph={graph}
            compatibility={compatibility}
          />
        </div>

        <section className="asymmetric-layout">

        <div className="left-stack">

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
            onPlay={handlePlay}
            onPause={handlePause}
            onNextStep={handleNextStep}
            onPrevStep={handlePrevStep}
            onResetSteps={handleResetSteps}
            isLoading={isLoading}
            isPlaying={isPlaying}
            stepControlsEnabled={stepControlsEnabled}
            isCompatible={compatibility.isCompatible}
            executionFinished={executionFinished}
          />


          <div className="card">
            <div className="card-title">Lecture pas à pas</div>

            {executionFinished && executionResult?.success ? (
              <div className="execution-finished-card">
                <div className="finish-icon" aria-hidden="true">
                  <svg
                    width="42"
                    height="42"
                    viewBox="0 0 42 42"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <rect
                      x="3"
                      y="3"
                      width="36"
                      height="36"
                      rx="10"
                      fill="#4f46e5"
                    />
                    <path
                      d="M12 21.5L18.2 27.5L30.5 14.5"
                      stroke="white"
                      strokeWidth="4"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>

            <div className="finish-title">
              Exécution terminée
            </div>

            <div className="finish-subtitle">
              Résultat final de l’algorithme
            </div>

            <div className="final-result-box">

              {(selectedAlgorithm==="dijkstra" ||
                selectedAlgorithm==="bellman-ford" ||
                selectedAlgorithm==="bellman") && (
                <>
                  <div className="r-label">
                    Chemin final
                  </div>

                  <div className="r-value">
                    {summary.path?.join(" → ") || "Aucun chemin n'existe"}
                  </div>

                  <div className="r-label final-label">
                    Distance
                  </div>

                  <div className="final-big-value">
                    {String(summary.distance ?? "—")}
                  </div>
                </>
              )}

              {(selectedAlgorithm==="prim" ||
                selectedAlgorithm==="kruskal") && (
                <>
                  <div className="r-label">
                    Nombre d’étapes
                  </div>

                  <div className="final-big-value">
                    {String(summary.total_cost ?? "—")}
                  </div>

                  <div className="r-label final-label">
                    Arêtes retenues
                  </div>

                  <div className="r-value">
                    {details.mst_edges?.join(", ") || "—"}
                  </div>
                </>
              )}

              {(selectedAlgorithm === "connected-components" ||
                selectedAlgorithm === "strongly-connected-components") && (
                <>
                  <div className="r-label">
                    Nombre de composantes
                  </div>

                  <div className="final-big-value">
                    {String(summary.count ?? "—")}
                  </div>

                  <div className="components-final-grid">
                    {(details.components || []).map((component: string[], index: number) => (
                      <div key={index} className="component-final-card">
                        <div className="component-final-title">
                          {selectedAlgorithm === "connected-components"
                            ? `Composante ${index + 1}`
                            : `CFC ${index + 1}`}
                        </div>

                        <div className="component-final-nodes">
                          {component.map((node: string) => (
                            <span key={node} className="component-final-node">
                              {node}
                            </span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              )}

              {selectedAlgorithm==="euler" && (
                <>
                  <div className="r-label">
                    Chemin eulérien
                  </div>

                  <div className="r-value">
                    {details.path?.join(" → ") || "Aucun chemin n'est trouvé"}
                  </div>
                </>
              )}

              {selectedAlgorithm==="welsh-powell" && (
                <>
                  <div className="r-label">
                    Nombre de couleurs
                  </div>

                  <div className="final-big-value">
                    {String(summary.color_count ?? "—")}
                  </div>

                  <div className="r-value">
                    {
                      Object.entries(
                        details.node_colors || {}
                      )
                      .map(
                        ([n,c])=>`${n}: ${c}`
                      )
                      .join(" | ")
                    }
                  </div>
                </>
              )}

              {(selectedAlgorithm === "ford-fulkerson" ||
                executionResult?.algorithm === "ford_fulkerson") && (
                <>
                  <div className="r-label">Flot maximum</div>

                  <div className="final-big-value">
                    {String(summary.max_flow ?? "—")}
                  </div>

                  <div className="r-label final-label">
                    Chemins augmentants
                  </div>

                  <div className="r-value">
                    {String(summary.augmenting_paths ?? "—")}
                  </div>
                </>
              )}

            </div>
          </div>

        ) : currentStep ? (

          <>
            <div className="step-focus-card">
        {/* <div className="step-topline">
          <span className="step-badge">
            Étape {currentStepIndex + 1}/{totalSteps}
          </span>

          <span className="step-type">
            {selectedAlgorithm === "connected-components"
              ? "Composantes connexes"
              : selectedAlgorithm === "strongly-connected-components"
              ? "Composantes fortement connexes"
              : "Algorithme"}
          </span>
        </div> */}

        <h3 className="step-title">
          {currentStep.title}
        </h3>

        <p className="step-description">
          {currentStep.description}
        </p>

        <div className="step-progress">
          <div
            className="step-progress-fill"
            style={{
              width: `${((currentStepIndex + 1) / totalSteps) * 100}%`,
            }}
          />
        </div>

        <div className="step-state-grid">

           {selectedAlgorithm === "kruskal" && (
          <div className="step-state-box sorted-edges-box">
            <div className="r-label">Arêtes triées par poids</div>

            <div className="edge-chip-row">
              {(
                currentStep?.state?.extra?.sorted_edges ||
                details?.sorted_edges ||
                details?.edge_list ||
                []
              ).map((edge: any, index: number) => (
                <span key={index} className="edge-chip">
                  {typeof edge === "string"
                    ? edge
                    : `${edge.source}-${edge.target} (${edge.weight})`}
                </span>
              ))}
            </div>
          </div>
        )}


        {(currentStep.state.highlighted_nodes || []).length > 0 && (
          <div className="step-state-box focus">
            <div className="r-label">
              {selectedAlgorithm === "connected-components" ||
              selectedAlgorithm === "strongly-connected-components"
                ? "Sommet exploré"
                : "Sommet en cours"}
            </div>

            <div className="node-chip-row">
              {(currentStep.state.highlighted_nodes || []).map((node: string) => (
                <span key={node} className="node-chip active">
                  {node}
                </span>
              ))}
            </div>
          </div>
        )}

        {(currentStep.state.visited_nodes || []).length > 0 &&
          selectedAlgorithm !== "connected-components" &&
          selectedAlgorithm !== "strongly-connected-components" && (
            <div className="step-state-box">
              <div className="r-label">Sommets visités</div>

              <div className="node-chip-row">
                {(currentStep.state.visited_nodes || []).map((node: string) => (
                  <span key={node} className="node-chip visited">
                    {node}
                  </span>
                ))}
              </div>
            </div>
          )}

        {(currentStep.state.selected_nodes || []).length > 0 && (
          <div className="step-state-box component-box">
            <div className="r-label">
              {selectedAlgorithm === "connected-components"
                ? "Composante en construction"
                : selectedAlgorithm === "strongly-connected-components"
                ? "CFC en construction"
                : "Sommets sélectionnés"}
            </div>

            <div className="node-chip-row component-row">
              {(currentStep.state.selected_nodes || []).map((node: string) => (
                <span key={node} className="node-chip selected">
                  {node}
                </span>
              ))}
            </div>
          </div>
        )}

        {(currentStep.state.selected_edges || []).length > 0 && (
          <div className="step-state-box">
            <div className="r-label">Arêtes sélectionnées</div>

            <div className="edge-chip-row">
              {(currentStep.state.selected_edges || []).map((edge: string) => (
                <span key={edge} className="edge-chip">
                  {edge}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
      </div>
          </>

        ) : (

          <div className="result-block">
            <div className="r-value">
              Aucune lecture en cours
            </div>
          </div>

        )}

      </div>

        </div>


        <div className="right-stack">
          <AlgorithmVisualizationCard
            graph={graph}
            executionResult={executionResult}
            currentStep={currentStep}
            sourceNode={sourceNode}
            targetNode={targetNode}
          />
        </div>

      </section>



      <section className="result-full">
        <AlgorithmResultCard
          executionResult={executionResult}
          isLoading={isLoading}
        />
      </section>
      </section>

      </main>

      </div>

      </div>
      );
      }