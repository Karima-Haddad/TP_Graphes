import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { FormuleGraphe } from "../components/FormuleGraphe";
import { VisualisationGraphe } from "../components/VisualisationGraphe";
import { PannelConfigGraphe } from "../components/PannelConfigGraphe";

import type { Graph } from "../types/graph.types";

import "../styles/App.css";

function GraphPage() {
  const [graph, setGraph] = useState<Graph | null>(() => {
    const saved = localStorage.getItem("graphData");

    if (!saved) return null;

    try {
      return JSON.parse(saved) as Graph;
    } catch {
      return null;
    }
  });
  const navigate = useNavigate();

  const goToAlgorithmPage = () => {
    if (!graph) {
      alert("Créer un graphe d'abord");
      return;
    }

    console.log("GRAPH COMPLET :", graph);
    console.log("ORIENTÉ ?", graph.directed);
    console.log("PONDÉRÉ ?", graph.weighted);
    console.log("ARÊTES :", graph.edges);

    localStorage.setItem("graphData", JSON.stringify(graph));

    navigate("/algorithm", {
      state: { graph },
    });
  };

  return (
    <div className="app-container">
      <header className="topbar">

      <div className="logo">
        <div className="logo-mark">
          <svg viewBox="0 0 18 18" fill="none">
            <circle cx="3.5" cy="3.5" r="2.5" fill="white"/>
            <circle cx="14.5" cy="3.5" r="2.5" fill="white"/>
            <circle cx="9" cy="14.5" r="2.5" fill="white"/>
            <line x1="5.8" y1="3.5" x2="12.2" y2="3.5" stroke="white" strokeWidth="1.3"/>
            <line x1="4.5" y1="5.5" x2="8" y2="12.5" stroke="white" strokeWidth="1.3"/>
            <line x1="13.5" y1="5.5" x2="10" y2="12.5" stroke="white" strokeWidth="1.3"/>
          </svg>
        </div>

        Graph<span>Lab</span>
      </div>


      <div className="topbar-nav">

        {/* page actuelle */}
        <button className="nav-tab done">
          1. Graphe prêt
        </button>


        {/* navigation vers page 2 */}
        <button
          className="nav-tab active"
          onClick={goToAlgorithmPage}
        >
          2. Algorithmes & résultats
        </button>

      </div>

    </header>


      <div className="app-layout">
        <div className="left-panel">
          <FormuleGraphe onGrapheCreé={setGraph} />
        </div>

        <div className="right-panel">
          <VisualisationGraphe
            graph={graph}
            onGraphChange={setGraph}
          />

          <div className="analysis-container">
            <PannelConfigGraphe graph={graph} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default GraphPage;