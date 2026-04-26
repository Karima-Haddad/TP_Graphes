import type { Graph } from '../types/graph.types';

const CLÉ_GRAPHE = 'graphe_application';
const CLÉ_HISTORIQUE = 'historique_graphes';

export const storageLocal = {
  sauvegarderGraphe: (graph: Graph): void => {
    try {
      localStorage.setItem(CLÉ_GRAPHE, JSON.stringify(graph));
    } catch (erreur) {
      console.error('Erreur lors de la sauvegarde du graphe:', erreur);
    }
  },

  obtenirGraphe: (): Graph | null => {
    try {
      const données = localStorage.getItem(CLÉ_GRAPHE);
      return données ? JSON.parse(données) : null;
    } catch (erreur) {
      console.error('Erreur lors de la récupération du graphe:', erreur);
      return null;
    }
  },

  ajouterAuHistorique: (graph: Graph): void => {
    try {
      const historique = storageLocal.obtenirHistorique();
      historique.push({
        ...graph,
        dateCreation: new Date().toISOString(),
      });
      localStorage.setItem(CLÉ_HISTORIQUE, JSON.stringify(historique));
    } catch (erreur) {
      console.error('Erreur lors de l\'ajout à l\'historique:', erreur);
    }
  },

  obtenirHistorique: (): (Graph & { dateCreation: string })[] => {
    try {
      const données = localStorage.getItem(CLÉ_HISTORIQUE);
      return données ? JSON.parse(données) : [];
    } catch (erreur) {
      console.error('Erreur lors de la récupération de l\'historique:', erreur);
      return [];
    }
  },

  effacerGraphe: (): void => {
    localStorage.removeItem(CLÉ_GRAPHE);
  },

  effacerTout: (): void => {
    localStorage.removeItem(CLÉ_GRAPHE);
    localStorage.removeItem(CLÉ_HISTORIQUE);
  },
};