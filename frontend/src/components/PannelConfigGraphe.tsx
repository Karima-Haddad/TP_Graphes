import React, { useState, useEffect } from 'react';
import type { Graph } from '../types/graph.types';
import { fetchGraphProperties } from '../services/executionApi';

interface PropsPannelConfigGraphe {
  graph: Graph | null;
}

interface GraphProperties {
  is_bipartite: boolean;
  is_tree: boolean;
  is_regular: boolean;
  is_eulerian: boolean;
}

export const PannelConfigGraphe: React.FC<PropsPannelConfigGraphe> = ({ graph }) => {
  const [statistiques, setStatistiques] = useState({
    sommets: 0,
    aretes: 0,
    connexe: false,
    cycles: 0,
    biparti: false,
  });

  const [graphProperties, setGraphProperties] = useState<GraphProperties>({
    is_bipartite: false,
    is_tree: false,
    is_regular: false,
    is_eulerian: false,
  });

  useEffect(() => {
    if (graph) {
      // eslint-disable-next-line react-hooks/immutability
      analyserGraphe();
      // eslint-disable-next-line react-hooks/immutability
      loadGraphProperties();
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

  const loadGraphProperties = async () => {
    if (!graph) return;

    try {
      const response = await fetchGraphProperties(graph);
      setGraphProperties({
        is_bipartite: response.result.is_bipartite,
        is_tree: response.result.is_tree,
        is_regular: response.result.is_regular,
        is_eulerian: response.result.is_eulerian,
      });
    } catch (error) {
      console.error('Erreur fetch graph properties:', error);
    }
  };

  const detecterCycles = (): number => {
    if (!graph) return 0;
    return graph.edges.length - (graph.nodes.length - 1) > 0 ? 1 : 0;
  };

  return (
    <>
      {/* STATISTIQUES RAPIDES */}
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

      {/* PROPRIÉTÉS STRUCTURELLES */}
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
            <span className="si-val">{statistiques.cycles > 0 ? 'Oui' : 'Non'}</span>
          </div>
        </div>
      </div>

      {/* ANALYSES COMPLÉMENTAIRES */}
      <div className="card">
        <div className="card-title">Analyses complémentaires</div>
        <div className="side-list">
          <div className={`si ${graphProperties.is_bipartite ? 'pass' : 'warn'}`}>
            <span className="si-icon"></span>
            Biparti
            <span className="si-val">
              {graphProperties.is_bipartite ? 'Oui' : 'Non'}
            </span>
          </div>
          <div className={`si ${graphProperties.is_tree ? 'pass' : 'warn'}`}>
            <span className="si-icon"></span>
            Arbre
            <span className="si-val">
              {graphProperties.is_tree ? 'Oui' : 'Non'}
            </span>
          </div>
          <div className={`si ${graphProperties.is_regular ? 'pass' : 'warn'}`}>
            <span className="si-icon"></span>
            Régulier
            <span className="si-val">
              {graphProperties.is_regular ? 'Oui' : 'Non'}
            </span>
          </div>
          <div className={`si ${graphProperties.is_eulerian ? 'pass' : 'warn'}`}>
            <span className="si-icon"></span>
            Eulérien
            <span className="si-val">
              {graphProperties.is_eulerian ? 'Oui' : 'Non'}
            </span>
          </div>
        </div>
      </div>
    </>
  );
};