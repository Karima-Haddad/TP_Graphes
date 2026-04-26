import React, { useState, useEffect } from 'react';
import type { Graph } from '../types/graph.types';
import '../styles/PannelConfigGraphe.css';

interface PropsPannelConfigGraphe {
  graph: Graph | null;
}

export const PannelConfigGraphe: React.FC<PropsPannelConfigGraphe> = ({ graph }) => {
  const [statistiques, setStatistiques] = useState({
    sommets: 0,
    aretes: 0,
    connexe: false,
    cycles: 0,
    biparti: false,
  });

  useEffect(() => {
    if (graph) {
      analyserGraphe();
    }
  }, [graph]);

  const analyserGraphe = () => {
    if (!graph) return;

    const sommets = graph.nodes.length;
    const aretes = graph.edges.length;

    setStatistiques({
      sommets,
      aretes,
      connexe: true,
      cycles: detecterCycles(),
      biparti: false,
    });
  };

  const detecterCycles = (): number => {
    if (!graph) return 0;
    return graph.edges.length - (graph.nodes.length - 1) > 0 ? 1 : 0;
  };

  return (
    <div className="panel-config">
      <div className="card">
        <div className="card-title">Statistiques rapides</div>
        <div className="stats">
          <div className="stat">
            <div className="stat-label">Sommets</div>
            <div className="stat-value">{statistiques.sommets}</div>
          </div>
          <div className="stat">
            <div className="stat-label">Arêtes</div>
            <div className="stat-value">{statistiques.aretes}</div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-title">Propriétés structurelles</div>
        <div className="side-list">
          <div className={`si ${statistiques.connexe ? 'pass' : 'warn'}`}>
            <span className="si-icon"></span>
            Connexe
            <span className="si-val">{statistiques.connexe ? 'Oui' : 'Non'}</span>
          </div>
          <div className="si info">
            <span className="si-icon"></span>
            Orientation
            <span className="si-val">{graph?.directed ? 'Orienté' : 'Non orienté'}</span>
          </div>
          <div className={`si ${graph?.weighted ? 'pass' : 'neutral'}`}>
            <span className="si-icon"></span>
            Pondération
            <span className="si-val">{graph?.weighted ? 'Oui' : 'Non'}</span>
          </div>
          <div className={`si ${statistiques.cycles > 0 ? 'warn' : 'pass'}`}>
            <span className="si-icon"></span>
            Cycle détecté
            <span className="si-val">{statistiques.cycles}</span>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-title">Analyses complémentaires</div>
        <div className="side-list">
          <div className="si neutral">
            <span className="si-icon"></span>
            Biparti
            <span className="si-val">Non</span>
          </div>
          <div className="si neutral">
            <span className="si-icon"></span>
            Arbre
            <span className="si-val">Non</span>
          </div>
          <div className="si neutral">
            <span className="si-icon"></span>
            Régulier
            <span className="si-val">Non</span>
          </div>
          <div className="si neutral">
            <span className="si-icon"></span>
            Eulérien
            <span className="si-val">Non</span>
          </div>
        </div>
      </div>
    </div>
  );
};