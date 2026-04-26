import React, { useState } from 'react';
import { FormuleGraphe } from './components/FormuleGraphe';
import { VisualisationGraphe } from './components/VisualisationGraphe';
import { PannelConfigGraphe } from './components/PannelConfigGraphe';
import type { Graph } from './types/graph.types';
import './styles/App.css';

function App() {
  const [graph, setGraph] = useState<Graph | null>(null);

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            <span className="icon">◆</span>
            Graph Lab
          </h1>
          <div className="header-tabs">
            <button className="tab active">1. Graphe</button>
            <button className="tab">2. Algorithme & résultat</button>
          </div>
        </div>
      </header>

      <div className="app-layout">
        {/* LEFT PANEL - INPUTS */}
        <div className="left-panel">
          <FormuleGraphe onGrapheCreé={setGraph} />
        </div>

        {/* RIGHT PANEL - VISUALIZATION & ANALYSIS */}
        <div className="right-panel">
          {/* VISUALIZATION */}
          <VisualisationGraphe graph={graph} />

          {/* ANALYSIS SECTION */}
          <div className="analysis-container">
            <PannelConfigGraphe graph={graph} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;