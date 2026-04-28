import type { AlgorithmOption } from "../types/algorithm.types";

export const ALGORITHMS: AlgorithmOption[] = [
  {
    key: "dijkstra",
    label: "Dijkstra",
    category: "Plus court chemin",
    requiresSource: true,
    requiresTarget: true,
    requiresWeighted: true,
    description:
      "Calcule le plus court chemin depuis un sommet source dans un graphe pondéré à poids positifs.",
  },
  {
    key: "bellman-ford",
    label: "Bellman-Ford",
    category: "Plus court chemin",
    requiresSource: true,
    requiresTarget: true,
    requiresWeighted: true,
    description:
      "Calcule les plus courts chemins et supporte les poids négatifs.",
  },
  {
    key: "bellman",
    label: "Bellman",
    category: "Plus court chemin",
    requiresSource: true,
    requiresTarget: true,
    requiresWeighted: true,
    description:
      "Variante du calcul de plus court chemin selon votre cours.",
  },
  {
    key: "kruskal",
    label: "Kruskal",
    category: "Arbre couvrant",
    requiresWeighted: true,
    description:
      "Construit un arbre couvrant minimum en triant les arêtes.",
  },
  {
    key: "prim",
    label: "Prim",
    category: "Arbre couvrant",
    requiresSource: true,
    requiresWeighted: true,
    description:
      "Construit un arbre couvrant minimum à partir d’un sommet de départ.",
  },
  {
    key: "connected-components",
    label: "Composantes connexes",
    category: "Connexité",
    description:
      "Détecte les composantes connexes d’un graphe non orienté.",
  },
  {
    key: "strongly-connected-components",
    label: "CFC",
    category: "Connexité",
    requiresDirected: true,
    description:
      "Détecte les composantes fortement connexes d’un graphe orienté.",
  },
  {
    key: "euler",
    label: "Chemins eulériens",
    category: "Autres",
    description:
      "Recherche un chemin ou circuit eulérien dans le graphe.",
  },
  {
    key: "welsh-powell",
    label: "Welsh-Powell",
    category: "Autres",
    description:
      "Coloration des sommets avec une heuristique gloutonne.",
  },
  {
  key: "ford-fulkerson",
  label: "Ford-Fulkerson",
  category: "Autres",
  requiresSource: true,
  requiresTarget: true,
  requiresWeighted: true,
  requiresDirected: true,
  description:
    "Calcule le flot maximum entre une source et un puits.",
 },
];