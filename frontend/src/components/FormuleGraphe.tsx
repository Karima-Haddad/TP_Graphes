import React, { useState, useEffect } from 'react';
import type { Graph, GraphNode, GraphEdge } from '../types/graph.types';
import { storageLocal } from '../services/storageLocal';
import '../styles/FormuleGraphe.css';

interface PropsFormuleGraphe {
  onGrapheCreé: (graph: Graph) => void;
}

export const FormuleGraphe: React.FC<PropsFormuleGraphe> = ({ onGrapheCreé }) => {
  const [representation, setRepresentation] = useState('liste');
  const [orientation, setOrientation] = useState('non-orienté');
  const [ponderation, setPonderation] = useState('pondéré');
  const [nombreSommets, setNombreSommets] = useState('5');
  const [listeSommets, setListeSommets] = useState('A, B, C, D, E');
  const [aretes, setAretes] = useState('A,B,4\nA,C,2\nB,D,5\nC,D,1\nD,E,3');
  const [feedback, setFeedback] = useState<{
    type: 'success' | 'error' | 'info';
    text: string;
  } | null>(null);
  const [matrice, setMatrice] = useState<string[][]>([
    ['0', '4', '2', '0', '0'],
    ['4', '0', '0', '5', '0'],
    ['2', '0', '0', '1', '0'],
    ['0', '5', '1', '0', '3'],
    ['0', '0', '0', '3', '0'],
  ]);


  useEffect(() => {
    const graph = storageLocal.obtenirGraphe();
    if (!graph) return;

    setOrientation(graph.directed ? "orienté" : "non-orienté");
    setPonderation(graph.weighted ? "pondéré" : "non-pondéré");
    setRepresentation("liste");

    setNombreSommets(String(graph.nodes.length));
    setListeSommets(graph.nodes.map((n) => n.label ?? n.id).join(", "));

    const edgesText = graph.edges
      .map((e) => {
        if (graph.weighted) {
          return `${e.source},${e.target},${e.weight ?? e.label ?? 1}`;
        }
        return `${e.source},${e.target}`;
      })
      .join("\n");

    setAretes(edgesText);

    // reconstruire la matrice aussi
    const labels = graph.nodes.map((n) => n.id);
    const n = labels.length;

    const newMatrice = Array.from({ length: n }, () =>
      Array.from({ length: n }, () => "0")
    );

    graph.edges.forEach((edge) => {
      const i = labels.indexOf(edge.source);
      const j = labels.indexOf(edge.target);

      if (i === -1 || j === -1) return;

      const value = graph.weighted ? String(edge.weight ?? 1) : "1";

      newMatrice[i][j] = value;

      if (!graph.directed && i !== j) {
        newMatrice[j][i] = value;
      }
    });

    setMatrice(newMatrice);
  }, []);


  useEffect(() => {
    const nombre = parseInt(nombreSommets);

    if (!isNaN(nombre) && nombre > 0 && matrice.length !== nombre) {
      initialiserMatrice(nombre);
    }
  }, [nombreSommets]);
  // useEffect(() => {
  //   const nombre = parseInt(nombreSommets);
  //   if (!isNaN(nombre) && nombre > 0) {
  //     initialiserMatrice(nombre);
  //   }
  // }, [nombreSommets]);

  const initialiserMatrice = (nombre: number) => {
    const newMatrice: string[][] = [];
    for (let i = 0; i < nombre; i++) {
      const row: string[] = [];
      for (let j = 0; j < nombre; j++) {
        row.push('0');
      }
      newMatrice.push(row);
    }
    setMatrice(newMatrice);
  };

  const updateMatriceCell = (row: number, col: number, value: string) => {
    if (row < 0 || row >= matrice.length || col < 0 || col >= matrice[row].length) {
      return;
    }

    const newMatrice = matrice.map((r, idx) => {
      if (idx === row) {
        return r.map((cell, colIdx) => (colIdx === col ? value : cell));
      }
      return [...r];
    });

    setMatrice(newMatrice);
  };

  const validerNombreSommets = (): { valide: boolean; message: string } => {
    const nombre = parseInt(nombreSommets);

    if (isNaN(nombre) || nombre < 0) {
      return { valide: false, message: 'Le nombre de sommets doit être supérieur ou égal à 0' };
    }

    return { valide: true, message: '' };
  };

  const validerListeSommets = (): {
    valide: boolean;
    message: string;
    sommets: string[];
  } => {
    const nombreAttendu = parseInt(nombreSommets);

    // cas graphe vide
    if (nombreAttendu === 0) {
      return { valide: true, message: '', sommets: [] };
    }

    const sommetsTexte = listeSommets
      .split(',')
      .map(s => s.trim())
      .filter(s => s.length > 0);

    // 🔥 ERREUR PRINCIPALE (ton besoin)
    if (sommetsTexte.length !== nombreAttendu) {
      return {
        valide: false,
        message: `Nombre de sommets incorrect ❌ (${sommetsTexte.length}/${nombreAttendu})`,
        sommets: [],
      };
    }

    // doublons
    if (new Set(sommetsTexte).size !== sommetsTexte.length) {
      return {
        valide: false,
        message: 'Les sommets ne doivent pas être dupliqués ❌',
        sommets: [],
      };
    }

    return { valide: true, message: '', sommets: sommetsTexte };
  };

  const validerAretes = (sommetsValides: string[]): { valide: boolean; message: string; edges: GraphEdge[] } => {
    const aretesTexte = aretes
      .split('\n')
      .map(a => a.trim())
      .filter(a => a.length > 0);

    if (aretesTexte.length === 0) {
      return { valide: true, message: '', edges: [] };
    }

    const edges: GraphEdge[] = [];
    const sommetsSet = new Set(sommetsValides);

    for (let i = 0; i < aretesTexte.length; i++) {
      const areteTexte = aretesTexte[i];
      const parts = areteTexte.split(',').map(s => s.trim());

      if (parts.length < 2) {
        return {
          valide: false,
          message: `❌ Ligne ${i + 1}: Format invalide`,
          edges: [],
        };
      }

      const source = parts[0];
      const target = parts[1];
      const weightStr = parts[2];

      if (!sommetsSet.has(source)) {
        return {
          valide: false,
          message: `❌ Ligne ${i + 1}: Le sommet "${source}" n'existe pas`,
          edges: [],
        };
      }

      if (!sommetsSet.has(target)) {
        return {
          valide: false,
          message: `❌ Ligne ${i + 1}: Le sommet "${target}" n'existe pas`,
          edges: [],
        };
      }

      // Les boucles (A,A) sont autorisées ✅
      if (ponderation === 'pondéré') {
        if (!weightStr || weightStr.length === 0) {
          return {
            valide: false,
            message: `❌ Ligne ${i + 1}: Le poids est obligatoire`,
            edges: [],
          };
        }

        const weight = parseInt(weightStr);
        if (isNaN(weight)) {
          return {
            valide: false,
            message: `❌ Ligne ${i + 1}: Le poids doit être un nombre`,
            edges: [],
          };
        }

        edges.push({
          id: `${source}-${target}-${i}`,
          source,
          target,
          weight,
          label: String(weight),
        });
      } else {
        edges.push({
          id: `${source}-${target}-${i}`,
          source,
          target,
        });
      }
    }

    return { valide: true, message: '', edges };
  };

  const validerMatrice = (sommetsValides: string[]): { valide: boolean; message: string; edges: GraphEdge[] } => {
    const n = sommetsValides.length;
    const edges: GraphEdge[] = [];

    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        const value = matrice[i][j];
        
        if (value === '' || value === '-') {
          return {
            valide: false,
            message: `❌ Cellule [${i + 1}][${j + 1}]: Doit être un nombre`,
            edges: [],
          };
        }

        const num = parseInt(value);
        if (isNaN(num)) {
          return {
            valide: false,
            message: `❌ Cellule [${i + 1}][${j + 1}]: Doit être un nombre`,
            edges: [],
          };
        }

        // Pour graphe non orienté, la matrice doit être symétrique
        // Exception: les boucles peuvent avoir n'importe quelle valeur
        if (orientation === 'non-orienté' && i !== j) {
          const numTranspose = parseInt(matrice[j][i]);
          if (num !== numTranspose) {
            return {
              valide: false,
              message: `❌ Matrice non symétrique: [${i + 1}][${j + 1}] ≠ [${j + 1}][${i + 1}]`,
              edges: [],
            };
          }
        }

        // Si pondéré, accepter tous les nombres
        // Si non pondéré, accepter seulement 0 et 1
        if (ponderation === 'non-pondéré') {
          if (num !== 0 && num !== 1) {
            return {
              valide: false,
              message: `❌ Cellule [${i + 1}][${j + 1}]: Utilisez seulement 0 ou 1`,
              edges: [],
            };
          }
        }

        // Créer les arêtes
        if (num !== 0) {
          if (orientation === 'non-orienté') {
            // Pour non orienté, ajouter une arête uniquement si i <= j pour éviter les doublons
            // i === j permet les boucles
            if (i <= j) {
              edges.push({
                id: `${sommetsValides[i]}-${sommetsValides[j]}-${i}-${j}`,
                source: sommetsValides[i],
                target: sommetsValides[j],
                weight: ponderation === 'pondéré' ? num : undefined,
                label: ponderation === 'pondéré' ? String(num) : undefined,
              });
            }
          } else {
            // Pour orienté, ajouter chaque arête (incluant les boucles)
            edges.push({
              id: `${sommetsValides[i]}-${sommetsValides[j]}-${i}-${j}`,
              source: sommetsValides[i],
              target: sommetsValides[j],
              weight: ponderation === 'pondéré' ? num : undefined,
              label: ponderation === 'pondéré' ? String(num) : undefined,
            });
          }
        }
      }
    }

    return { valide: true, message: '', edges };
  };

  const creerGraphe = () => {
    try {
      const validNombre = validerNombreSommets();
      if (!validNombre.valide) {
        setFeedback({ type: 'error', text: validNombre.message });
        return;
      }

      const validSommets = validerListeSommets();
      if (!validSommets.valide) {
        setFeedback({ type: 'error', text: validSommets.message });
        return;
      }

      let edges;

      if (representation === 'liste') {
        const validAretes = validerAretes(validSommets.sommets);
        if (!validAretes.valide) {
          setFeedback({ type: 'error', text: validAretes.message });
          return;
        }
        edges = validAretes.edges;
      } else {
        const validMatrice = validerMatrice(validSommets.sommets);
        if (!validMatrice.valide) {
          setFeedback({ type: 'error', text: validMatrice.message });
          return;
        }
        edges = validMatrice.edges;
      }

      const nodes: GraphNode[] = validSommets.sommets.map((label, index) => ({
        id: label,
        label,
        x: 100 + (index * 120) % 500,
        y: 100 + Math.floor(index / 4) * 120,
      }));

      const graph: Graph = {
        directed: orientation === 'orienté',
        weighted: ponderation === 'pondéré',
        nodes,
        edges,
      };

      storageLocal.sauvegarderGraphe(graph);
      storageLocal.ajouterAuHistorique(graph);
      onGrapheCreé(graph);

    //   setFeedback({
    //   type: 'success',
    //   text: 'Graphe créé avec succès'
    // });
    } catch (erreur) {
      setFeedback({
        type: 'error',
        text: `Erreur inattendue : ${erreur}`
      });
    }
  };

  const réinitialiser = () => {
    setOrientation('non-orienté');
    setPonderation('pondéré');
    setRepresentation('liste');
    setNombreSommets('5');
    setListeSommets('A, B, C, D, E');
    setAretes('A,B,4\nA,C,2\nB,D,5\nC,D,1\nD,E,3');
    initialiserMatrice(5);
    storageLocal.effacerGraphe();
    setFeedback(null);
    onGrapheCreé({
      directed: false,
      weighted: true,
      nodes: [],
      edges: [],
    });
  };


  const sommetsArray = listeSommets.split(',').map(s => s.trim());

  return (
    <div className="formule-graphe">
      <div className="card">
        <div className="card-title">Configuration du graphe</div>

        {feedback && (
          <div className={`feedback ${feedback.type}`}>
            <span className="icon">
              {feedback.type === 'success' && '✔'}
              {feedback.type === 'error' && '⚠'}
              {feedback.type === 'info' && 'ℹ'}
            </span>
            <span>{feedback.text}</span>
          </div>
        )}

        {/* ROW 1: Mode et Représentation */}
        <div className="form-row">
          <div className="field">
            <label>Représentation</label>
            <select value={representation} onChange={(e) => setRepresentation(e.target.value)}>
              <option value="liste">Liste d'arêtes</option>
              <option value="matrice">Matrice d'adjacence</option>
            </select>
          </div>
        </div>

        {/* ROW 2: Orientation et Pondération */}
        <div className="form-row">
          <div className="field">
            <label>Orientation</label>
            <select value={orientation} onChange={(e) => setOrientation(e.target.value)}>
              <option value="non-orienté">Non orienté</option>
              <option value="orienté">Orienté</option>
            </select>
          </div>
          <div className="field">
            <label>Pondération</label>
            <select value={ponderation} onChange={(e) => setPonderation(e.target.value)}>
              <option value="pondéré">Pondéré</option>
              <option value="non-pondéré">Non pondéré</option>
            </select>
          </div>
        </div>

        {/* ROW 3: Nombre et Liste des sommets */}
        <div className="form-row">
          <div className="field">
            <label>Nombre de sommets *</label>
            <input
              type="number"
              min="1"
              value={nombreSommets}
              onChange={(e) => setNombreSommets(e.target.value)}
            />
          </div>
          <div className="field">
            <label>Liste des sommets *</label>
            <input
              type="text"
              value={listeSommets}
              onChange={(e) => setListeSommets(e.target.value)}
              placeholder="A, B, C, D, E"
            />
          </div>
        </div>

        {/* SECTION: LISTE D'ARÊTES */}
        {representation === 'liste' && (
          <div className="section">
            <div className="section-title">Arêtes</div>
            <textarea
              value={aretes}
              onChange={(e) => setAretes(e.target.value)}
              placeholder={
                ponderation === 'pondéré'
                  ? 'A,B,4\nA,C,2\nA,A,1 (boucle)'
                  : 'A,B\nA,C\nA,A (boucle)'
              }
              className="aretes-textarea"
            />
            <div className="section-hint">
              • Format: {ponderation === 'pondéré' ? 'source,destination,poids' : 'source,destination'} <br></br>
              • Les boucles (A,A) sont acceptées ✅
            </div>
          </div>
        )}

        {/* SECTION: MATRICE */}
        {representation === 'matrice' && (
          <div className="section">
            <div className="section-title">Matrice d'adjacence</div>
            <div className="matrice-scroll">
              <table className="matrice-table">
                <thead>
                  <tr>
                    <th className="matrice-th corner"></th>
                    {sommetsArray.map((s) => (
                      <th key={`h-${s}`} className="matrice-th">
                        {s}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {matrice.map((row, i) => (
                    <tr key={`r-${i}`}>
                      <th className="matrice-th label">{sommetsArray[i]}</th>
                      {row.map((cell, j) => (
                        <td key={`c-${i}-${j}`} className={`matrice-td ${i === j ? 'diagonal' : ''}`}>
                          <input
                            type="text"
                            inputMode="numeric"
                            value={cell}
                            onChange={(e) => {
                              const val = e.target.value;
                              if (val === '' || val === '-' || !isNaN(Number(val))) {
                                updateMatriceCell(i, j, val);
                              }
                            }}
                            onBlur={(e) => {
                              if (e.target.value === '' || e.target.value === '-') {
                                updateMatriceCell(i, j, '0');
                              }
                            }}
                            className="matrice-input"
                          />
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="section-hint">
              {orientation === 'non-orienté' && '•  Matrice symétrique requise (sauf diagonale)'}<br />
              {ponderation === 'non-pondéré' && ' • Utilisez 0 ou 1'}
              {ponderation === 'pondéré' && ' • Utilisez des nombres'}
              <br />
              • Les boucles (diagonale) sont acceptées
            </div>
          </div>
        )}

        {/* BUTTONS */}
        <div className="btn-row">
          <button className="btn btn-primary" onClick={creerGraphe}>
            Créer le graphe
          </button>
          <button className="btn btn-secondary" onClick={réinitialiser}>
            Réinitialiser
          </button>
        </div>
      </div>
    </div>
  );
};