# 🎨 Frontend - Plateforme de Graphes

Interface web interactive pour créer, visualiser et analyser des graphes avec une suite d'algorithmes avancés. Développé avec **React 19**, **TypeScript** et **Vite**.

## 📋 Table des matières

- [🚀 Démarrage Rapide](#-démarrage-rapide)
- [📁 Structure du Projet](#-structure-du-projet)
- [🎯 Fonctionnalités](#-fonctionnalités)
- [🔌 Intégration API](#-intégration-api)
- [🎨 Composants](#-composants)
- [📝 Types TypeScript](#-types-typescript)
- [🛠️ Services](#-services)
- [💅 Styles](#-styles)
- [🧪 Linting](#-linting)
- [🔧 Configuration](#-configuration)

---

## 🚀 Démarrage Rapide

### Prérequis

- **Node.js** 18+
- **npm** ou **yarn**

### Installation

```bash
cd frontend
npm install
```

### Démarrage en développement

```bash
npm run dev
```

L'application sera accessible sur : **`http://localhost:5173`**

### Build pour production

```bash
npm run build
```

Les fichiers optimisés seront générés dans le répertoire `dist/`

### Preview production

```bash
npm run preview
```

---


## 🧪 Guide de test interactif

Dans le cadre de la validation du projet, un guide de test complet a été conçu sous forme d’interface HTML interactive.

🔗 Accès :
http://localhost:5173/test.html

**🎯 Objectif**
Faciliter la vérification du comportement des algorithmes sur différents types de graphes.

**📌 Contenu**
- Tests pour tous les algorithmes (Dijkstra, Prim, Kruskal, Euler, etc.)
- Cas normaux
- Cas limites
- Cas extrêmes
- Cas sans solution
- Résultats attendus pour chaque scénario

**💡 Utilisation**
Lancer l’application frontend puis accéder à l’URL ci-dessus pour explorer les tests.


- Ce guide a été utilisé par l’équipe pour garantir la robustesse et la fiabilité du système.

---

## 📁 Structure du Projet

```
frontend/
├── index.html                   # Point d'entrée HTML
├── package.json                 # Dépendances et scripts
├── vite.config.ts              # Configuration Vite
├── tsconfig.json               # Configuration TypeScript (générale)
├── tsconfig.app.json           # Configuration TypeScript (app)
├── tsconfig.node.json          # Configuration TypeScript (node)
├── eslint.config.js            # Configuration ESLint
│
├── src/
│   ├── main.tsx                # Point d'entrée React
│   ├── App.tsx                 # Composant racine
│   ├── App.css                 # Styles globaux
│   ├── index.css               # Styles de base
│   │
│   ├── pages/                  # Pages principales (Routes)
│   │   ├── index.ts            # Export des pages
│   │   ├── GraphPage.tsx       # Page: Gestion des graphes
│   │   ├── CréationGraphe.tsx  # Page: Création de graphes
│   │   └── AlgorithmPage.tsx   # Page: Exécution d'algorithmes
│   │
│   ├── components/             # Composants réutilisables
│   │   ├── index.ts            # Exports barrel
│   │   ├── FormuleGraphe.tsx       # Form. création graphe
│   │   ├── VisualisationGraphe.tsx # Affichage graphique
│   │   ├── PannelConfigGraphe.tsx  # Panel configuration
│   │   ├── AlgorithmSidebar.tsx    # Barre latérale algos
│   │   ├── AlgorithmInfoCard.tsx   # Carte info algo
│   │   ├── AlgorithmParamsCard.tsx # Carte paramètres
│   │   ├── AlgorithmResultCard.tsx # Carte résultats
│   │   └── AlgorithmVisualizationCard.tsx # Carte visualisation
│   │
│   ├── services/               # Appels API et logique
│   │   ├── executionApi.ts     # API exécution algorithmes
│   │   ├── graphPropertiesApi.ts  # API propriétés graphes
│   │   └── storageLocal.ts     # Gestion du stockage local
│   │
│   ├── types/                  # Définitions TypeScript
│   │   ├── graph.types.ts      # Types: Graph, Edge, Node
│   │   ├── algorithm.types.ts  # Types: Algorithm, Params
│   │   ├── execution.types.ts  # Types: Execution, Results
│   │   └── executionResponse.types.ts # Types: Réponses API
│   │
│   ├── utils/                  # Fonctions utilitaires
│   │   ├── buildExecutionParams.ts    # Construction paramètres
│   │   ├── buildExecutionRequest.ts   # Construction requête
│   │   └── checkAlgorithmCompatibility.ts # Vérification compat.
│   │
│   ├── styles/                 # Fichiers CSS modulaires
│   │   ├── App.css
│   │   ├── algorithm-page.css
│   │   ├── CréationGraphe.css
│   │   ├── FormuleGraphe.css
│   │   ├── PannelConfigGraphe.css
│   │   └── VisualisationGraphe.css
│   │
│   ├── assets/                 # Images, icônes, ressources
│   └── data/                   # Données statiques
│       └── algorithms.ts       # Métadonnées algorithmes
│
├── public/                     # Ressources statiques
│   ├── test.html
│   └── [autres ressources]
│
└── dist/                       # Build production (généré)
```

---

## 🎯 Fonctionnalités

### 📊 Création de Graphes
- ✏️ Interface intuitive pour ajouter/supprimer sommets
- 🔗 Interface pour ajouter/supprimer arêtes
- ⚙️ Configuration (orienté/non-orienté, pondérés)
- 💾 Sauvegarde automatique en localStorage

### 📈 Visualisation
- 🎨 Rendu interactif des graphes
- 🖱️ Drag & drop pour repositionner les nœuds
- 🔍 Zoom et pan
- 📍 Vue d'ensemble et détails

### 🧮 Algorithmes
- **Chemins les plus courts** : Dijkstra, Bellman-Ford
- **Arbres couvrants** : Kruskal, Prim
- **Flot maximal** : Ford-Fulkerson
- **Analyse structurelle** : Composantes connexes, SCC
- **Coloration** : Welsh-Powell
- **Circuits** : Chemin Eulérien

### 📊 Résultats
- 📋 Affichage détaillé des résultats
- 📈 Graphiques et tableaux
- ⏱️ Temps d'exécution
- 🔄 Animation des étapes

---

## 🔌 Intégration API

### Configuration API

L'API backend est accessible sur : **`http://localhost:8000`**

### Appels API

#### Exécuter un algorithme

```typescript
POST /api/[route]/[algorithm]
Content-Type: application/json

{
  "graph": {
    "nodes": ["A", "B", "C"],
    "edges": [
      {"source": "A", "target": "B", "weight": 4},
      {"source": "B", "target": "C", "weight": 2}
    ],
    "directed": false
  },
  "start": "A"  // optionnel, selon l'algorithme
}
```

#### Réponse

```json
{
  "success": true,
  "algorithm": "dijkstra",
  "result": {
    "distances": {"A": 0, "B": 4, "C": 6},
    "predecessor": {"A": null, "B": "A", "C": "B"}
  },
  "visualization": { /* données */ },
  "time_ms": 1.23
}
```

### Services API

#### `executionApi.ts`

```typescript
// Exécuter un algorithme
executeAlgorithm(
  algorithmRoute: string,
  algorithmName: string,
  payload: ExecutionRequest
): Promise<ExecutionResponse>

// Exécuter Dijkstra
executeDijkstra(graph: Graph, start: string): Promise<ExecutionResponse>

// Exécuter Bellman-Ford
executeBellmanFord(graph: Graph, start: string): Promise<ExecutionResponse>

// Exécuter Kruskal
executeKruskal(graph: Graph): Promise<ExecutionResponse>

// Exécuter Prim
executePrim(graph: Graph): Promise<ExecutionResponse>

// Exécuter Ford-Fulkerson
executeFordFulkerson(graph: Graph, source: string, sink: string): Promise<ExecutionResponse>
```

#### `graphPropertiesApi.ts`

```typescript
// Analyser les propriétés d'un graphe
analyzeGraph(graph: Graph): Promise<GraphProperties>

// Récupérer les composantes connexes
getConnectedComponents(graph: Graph): Promise<ExecutionResponse>

// Récupérer les composantes fortement connexes
getStronglyConnectedComponents(graph: Graph): Promise<ExecutionResponse>
```

#### `storageLocal.ts`

```typescript
// Sauvegarder un graphe
saveGraph(id: string, graph: Graph): void

// Charger un graphe
loadGraph(id: string): Graph | null

// Charger tous les graphes
loadAllGraphs(): Graph[]

// Supprimer un graphe
deleteGraph(id: string): void

// Exporter un graphe (JSON)
exportGraph(graph: Graph): string
```

---

## 🎨 Composants

### Pages

#### `GraphPage.tsx`
- Page principale : création et gestion de graphes
- Affiche la liste des graphes sauvegardés
- Permet de créer, charger, exporter des graphes

#### `CréationGraphe.tsx`
- Formulaire de création interactif
- Ajout/suppression de sommets
- Ajout/suppression d'arêtes
- Configuration du graphe

#### `AlgorithmPage.tsx`
- Sélection d'algorithme
- Configuration des paramètres
- Affichage des résultats
- Visualisation avec étapes

### Composants Réutilisables

#### `FormuleGraphe.tsx`
```typescript
interface FormuleGrapheProps {
  onGrapheCreé: (graph: Graph) => void;
  initialGraph?: Graph;
}
```
Composant formulaire pour créer/modifier un graphe.

#### `VisualisationGraphe.tsx`
```typescript
interface VisualisationGrapheProps {
  graph: Graph;
  highlighting?: HighlightingData;
  interactive?: boolean;
}
```
Composant de rendu SVG/Canvas pour afficher le graphe.

#### `PannelConfigGraphe.tsx`
```typescript
interface PannelConfigProps {
  graph: Graph;
  onConfigChange: (config: GraphConfig) => void;
}
```
Panneau de configuration avancée du graphe.

#### `AlgorithmSidebar.tsx`
```typescript
interface AlgorithmSidebarProps {
  algorithms: Algorithm[];
  onAlgorithmSelect: (algo: Algorithm) => void;
  selectedAlgorithm?: Algorithm;
}
```
Barre latérale avec liste des algorithmes.

#### `AlgorithmInfoCard.tsx`
```typescript
interface AlgorithmInfoCardProps {
  algorithm: Algorithm;
}
```
Carte d'information sur un algorithme (description, complexité).

#### `AlgorithmParamsCard.tsx`
```typescript
interface AlgorithmParamsCardProps {
  algorithm: Algorithm;
  onParamsChange: (params: ExecutionParams) => void;
}
```
Formulaire pour configurer les paramètres d'exécution.

#### `AlgorithmResultCard.tsx`
```typescript
interface AlgorithmResultCardProps {
  result: ExecutionResponse;
  algorithm: Algorithm;
}
```
Affichage des résultats d'exécution.

#### `AlgorithmVisualizationCard.tsx`
```typescript
interface AlgorithmVisualizationCardProps {
  result: ExecutionResponse;
  graph: Graph;
  currentStep?: number;
}
```
Visualisation des étapes d'exécution.

---

## 📝 Types TypeScript

### `graph.types.ts`

```typescript
interface Node {
  id: string;
  label: string;
  x?: number;
  y?: number;
}

interface Edge {
  source: string;
  target: string;
  weight?: number;
  capacity?: number;
  flow?: number;
}

interface Graph {
  nodes: Node[];
  edges: Edge[];
  directed: boolean;
  weighted?: boolean;
  name?: string;
}
```

### `algorithm.types.ts`

```typescript
interface Algorithm {
  id: string;
  name: string;
  description: string;
  complexity: string;
  category: "shortest-path" | "mst" | "flow" | "analysis" | "coloring";
  requirements: AlgorithmRequirement[];
  parameters: AlgorithmParameter[];
}

interface AlgorithmParameter {
  name: string;
  type: "string" | "number" | "boolean";
  description: string;
  required: boolean;
  default?: any;
}
```

### `execution.types.ts`

```typescript
interface ExecutionRequest {
  graph: Graph;
  [key: string]: any;  // Paramètres additionnels
}

interface ExecutionParams {
  start?: string;      // Pour chemins courts
  source?: string;     // Pour flot
  sink?: string;       // Pour flot
  [key: string]: any;
}

interface ExecutionResponse {
  success: boolean;
  algorithm: string;
  result: any;
  visualization: any;
  steps?: ExecutionStep[];
  time_ms: number;
  error?: string;
}

interface ExecutionStep {
  iteration: number;
  data: any;
  description: string;
}
```

### `executionResponse.types.ts`

```typescript
interface DijkstraResult {
  distances: Record<string, number>;
  predecessor: Record<string, string | null>;
  path?: string[];
}

interface MSTResult {
  mst_edges: Edge[];
  total_weight: number;
}

interface FordFulkersonResult {
  max_flow: number;
  flow_edges: FlowEdge[];
}

interface ColorizationResult {
  coloring: Record<string, number>;
  chromatic_number: number;
}
```

---

## 🛠️ Services

### Service: Exécution d'Algorithmes

```typescript
// src/services/executionApi.ts

class ExecutionApiService {
  private static readonly BASE_URL = "http://localhost:8000/api";

  static async executeAlgorithm(
    route: string,
    algorithm: string,
    payload: ExecutionRequest
  ): Promise<ExecutionResponse>

  static async executeDijkstra(
    graph: Graph,
    start: string
  ): Promise<ExecutionResponse>

  static async executeBellmanFord(
    graph: Graph,
    start: string
  ): Promise<ExecutionResponse>

  // ... autres méthodes
}
```

### Service: Propriétés Graphes

```typescript
// src/services/graphPropertiesApi.ts

class GraphPropertiesApiService {
  static async getConnectedComponents(
    graph: Graph
  ): Promise<ExecutionResponse>

  static async getStronglyConnectedComponents(
    graph: Graph
  ): Promise<ExecutionResponse>

  static async analyzeGraph(graph: Graph): Promise<GraphProperties>
}
```

### Service: Stockage Local

```typescript
// src/services/storageLocal.ts

class LocalStorageService {
  static saveGraph(id: string, graph: Graph): void
  static loadGraph(id: string): Graph | null
  static loadAllGraphs(): Graph[]
  static deleteGraph(id: string): void
  static exportGraph(graph: Graph): string
  static importGraph(json: string): Graph
}
```

---

## 💅 Styles

### Organisation CSS

```
src/styles/
├── App.css                    # Styles globaux
├── algorithm-page.css         # Page algorithmes
├── CréationGraphe.css         # Formulaire création
├── FormuleGraphe.css          # Composant formulaire
├── PannelConfigGraphe.css     # Panneau config
└── VisualisationGraphe.css    # Visualisation graphe
```

### Conventions

- **Variables CSS** : `--color-primary`, `--spacing-unit`
- **Classes** : `component-name`, `component-name__element`
- **Responsive** : Breakpoints mobiles à `768px`, `1024px`

### Thème

```css
:root {
  --color-primary: #2563eb;
  --color-secondary: #64748b;
  --color-success: #16a34a;
  --color-error: #dc2626;
  --color-bg: #ffffff;
  --color-text: #1e293b;
  --spacing-unit: 8px;
}
```

---

## 🧪 Linting

### Exécuter ESLint

```bash
npm run lint
```

### Corriger automatiquement

```bash
npm run lint -- --fix
```

### Configuration ESLint

Voir `eslint.config.js` pour les règles activées.

---

## 🔧 Configuration

### Vite (`vite.config.ts`)

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'terser'
  }
})
```

### TypeScript (`tsconfig.json`)

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "esModuleInterop": true,
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

---

## 📦 Dépendances Principales

### Production

| Package | Version | Utilité |
|---------|---------|---------|
| **react** | ^19.2.5 | Bibliothèque UI |
| **react-dom** | ^19.2.5 | Rendu DOM |
| **react-router-dom** | ^7.14.2 | Navigation SPA |

### Développement

| Package | Version | Utilité |
|---------|---------|---------|
| **vite** | ^8.0.9 | Bundler ultrarapide |
| **typescript** | ~6.0.2 | Typage statique |
| **eslint** | ^9.39.4 | Linting code |
| **@vitejs/plugin-react** | ^6.0.1 | Support JSX Vite |

---

## 🔄 Flux de Données

```
┌─────────────────────────────────┐
│     Pages (GraphPage, etc)      │
└────────────────┬────────────────┘
                 │
                 ↓
┌─────────────────────────────────┐
│      Composants (Form, etc)     │
└────────────────┬────────────────┘
                 │
                 ↓
┌─────────────────────────────────┐
│    Services (API, Storage)      │
└────────────────┬────────────────┘
                 │
        ┌────────┴────────┐
        ↓                 ↓
  Backend API      LocalStorage
```

---

## 🚀 Workflow Développement

### 1. Créer un nouveau composant

```typescript
// src/components/MyComponent.tsx
import React from 'react';

interface MyComponentProps {
  title: string;
  onSubmit: (data: any) => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({
  title,
  onSubmit
}) => {
  return (
    <div className="my-component">
      <h2>{title}</h2>
      {/* Contenu */}
    </div>
  );
};
```

### 2. Ajouter une page

```typescript
// src/pages/MyPage.tsx
import React from 'react';
import { MyComponent } from '../components';

export const MyPage: React.FC = () => {
  return (
    <div className="my-page">
      <h1>Ma Page</h1>
      <MyComponent title="Test" onSubmit={console.log} />
    </div>
  );
};
```

### 3. Ajouter une route

```typescript
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MyPage } from './pages';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/my-page" element={<MyPage />} />
      </Routes>
    </BrowserRouter>
  );
}
```

---

## 🐛 Debugging

### DevTools React

Installer l'extension React DevTools pour le navigateur.

### Logs Console

```typescript
console.log('Debug info:', data);
console.warn('Warning:', message);
console.error('Error:', error);
```

### Source Map

Activer les source maps en développement pour mieux déboguer:

```bash
# Déjà activé par défaut avec Vite
npm run dev
```

---

## 📚 Ressources

- [React Documentation](https://react.dev)
- [React Router Documentation](https://reactrouter.com)
- [TypeScript Documentation](https://www.typescriptlang.org)
- [Vite Documentation](https://vite.dev)
- [ESLint Documentation](https://eslint.org)

---

## 📋 Checklist Démarrage

- [ ] Node.js 18+ installé
- [ ] Dépendances installées (`npm install`)
- [ ] Backend lancé (`http://localhost:8000`)
- [ ] Frontend lancé (`npm run dev`)
- [ ] Accessible sur `http://localhost:5173`
- [ ] Console sans erreurs

---

## 🤝 Convention de Code

### Nommage

- **Fichiers composants** : `PascalCase` (ex: `MyComponent.tsx`)
- **Fichiers services** : `camelCase` (ex: `executionApi.ts`)
- **Variables** : `camelCase` (ex: `myVariable`)
- **Constantes** : `UPPER_SNAKE_CASE` (ex: `MAX_NODES`)

### Structure Composant

```typescript
// Imports
import React from 'react';

// Types/Interfaces
interface MyComponentProps {
  // ...
}

// Composant
export const MyComponent: React.FC<MyComponentProps> = (props) => {
  // Hooks
  const [state, setState] = React.useState();

  // Effects
  React.useEffect(() => {
    // ...
  }, []);

  // Handlers
  const handleClick = () => {
    // ...
  };

  // Render
  return (
    <div>
      {/* JSX */}
    </div>
  );
};
```

---

**Version** : 1.0.0  
**Dernière mise à jour** : Mai 2026  
**Auteur** : Équipe TP Graphes
