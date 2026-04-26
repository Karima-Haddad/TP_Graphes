import React, { useState, useEffect } from 'react';
import type { Graph } from '../types/graph.types';
import { storageLocal } from '../services/storageLocal';
import { FormuleGraphe } from '../components/FormuleGraphe';
import { VisualisationGraphe } from '../components/VisualisationGraphe';
import { PannelConfigGraphe } from '../components/PannelConfigGraphe';
import '../styles/CréationGraphe.css';

export const CréationGraphe: React.FC = () => {
  const [graph, setGraph] = useState<Graph | null>(null);

  useEffect(() => {
    const graphSauvegardé = storageLocal.obtenirGraphe();
    if (graphSauvegardé) {
      setGraph(graphSauvegardé);
    }
  }, []);

  const handleGrapheCreé = (nouveauGraphe: Graph) => {
    setGraph(nouveauGraphe);
  };

  return (
    <div className="creation-graphe">
      <header className="topbar">
        <div className="logo">
          <div className="logo-mark">
            <svg viewBox="0 0 18 18" fill="none">
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
        <nav className="topbar-nav">
          <div className="nav-tab active">1. Graphe</div>
          <div className="nav-tab inactive">2. Algorithme & résultat</div>
        </nav>
      </header>

      <main className="main">
        <section className="page-header">
          <div className="page-eyebrow">Page 01</div>
          <h1 className="page-title">Création et visualisation du graphe</h1>
          <p className="page-desc">
            Cette page est dédiée à la saisie ou à l'import du graphe, à sa visualisation et à
            l'analyse de ses propriétés principales avant de lancer un traitement algorithmique.
          </p>
        </section>

        <section className="grid grid-2">
          <div className="col">
            <FormuleGraphe onGrapheCreé={handleGrapheCreé} />
            <PannelConfigGraphe graph={graph} />
          </div>

          <div className="col">
            <VisualisationGraphe graph={graph} />
            <div className="btn-row" style={{ marginTop: '20px', justifyContent: 'flex-end' }}>
              <a className="btn btn-success" href="/page2_algorithme_resultat">
                Continuer vers les algorithmes →
              </a>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};