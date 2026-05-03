import React, { useState, useEffect } from 'react';
import type { Graph } from '../types/graph.types';
import { fetchGraphProperties } from '../services/graphPropertiesApi';


interface PropsPannelConfigGraphe {
  graph: Graph | null;
  mode?: 'stats' | 'analysis';
}

export const PannelConfigGraphe: React.FC<PropsPannelConfigGraphe> = ({ graph, mode = 'analysis' }) => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [loading, setLoading] = useState(false);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [error, setError] = useState<string | null>(null);

  const [statistiques, setStatistiques] = useState({
    sommets: 0,
    aretes: 0,
    connexe: false,
    cycles: 0,
    biparti: false,
    arbre: false,
    regulier: false,
    eulerien: false,
  });

  useEffect(() => {
    const analyserGraphe = async () => {
      if (!graph) return;

      setLoading(true);
      setError(null);

      try {
        const data = await fetchGraphProperties(graph);

        console.log("RÉPONSE PROPRIÉTÉS =", data);

        const props = data.result;

        setStatistiques({
          sommets: props.nodes_count ?? 0,
          aretes: props.edges_count ?? 0,
          connexe: props.is_connected ?? false,
          cycles: props.has_cycle ? 1 : 0,
          biparti: props.is_bipartite ?? false,
          arbre: props.is_tree ?? false,
          regulier: props.is_regular ?? false,
          eulerien: props.is_eulerian ?? false,
        });

      } catch (err) {
        setError("Erreur lors de l’analyse du graphe");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    analyserGraphe();
  }, [graph]);

  return (
    <>
    {/* STATISTIQUES RAPIDES */}
    {mode === "stats" && (
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

         )}
      {mode === "analysis" && (
      <>

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
          <div className={`si ${statistiques.biparti ? 'pass' : 'neutral'}`}>
            <span className="si-icon"></span>
            Biparti
            <span className="si-val">{statistiques.biparti ? 'Oui' : 'Non'}</span>
          </div>

          <div className={`si ${statistiques.arbre ? 'pass' : 'neutral'}`}>
            <span className="si-icon"></span>
            Arbre
            <span className="si-val">{statistiques.arbre ? 'Oui' : 'Non'}</span>
          </div>

          <div className={`si ${statistiques.regulier ? 'pass' : 'neutral'}`}>
            <span className="si-icon"></span>
            Régulier
            <span className="si-val">{statistiques.regulier ? 'Oui' : 'Non'}</span>
          </div>

          <div className={`si ${statistiques.eulerien ? 'pass' : 'neutral'}`}>
            <span className="si-icon"></span>
            Eulérien
            <span className="si-val">{statistiques.eulerien ? 'Oui' : 'Non'}</span>
          </div>
        </div>
      </div>
      </>
       )}
    </>
  );
};