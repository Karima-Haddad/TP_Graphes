# 🔧 Backend - Plateforme de Graphes

API REST FastAPI pour les algorithmes de graphes et visualisation.

## 📋 Table des matières

- [Installation](#-installation)
- [Démarrage](#-démarrage)
- [Structure](#-structure)
- [Endpoints API](#-endpoints-api)
- [Modèles de Données](#-modèles-de-données)
- [Algorithmes](#-algorithmes)
- [Tests](#-tests)
- [Architecture](#-architecture)

## 🛠️ Installation

### Prérequis

- **Python 3.9+**
- **pip** (gestionnaire de paquets Python)
- **Virtual Environment** (recommandé)

### Étapes d'Installation

#### 1. Créer un environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

#### 3. Vérifier l'installation

```bash
pip freeze
```

### Dépendances Principales

| Package | Version | Description |
|---------|---------|-------------|
| **FastAPI** | ≥0.128.0 | Framework web moderne et performant |
| **Uvicorn** | ≥0.27.0 | Serveur ASGI haute performance |
| **Pydantic** | Dernière | Validation de données avec typage |
| **Pytest** | ≥8.0 | Framework de testing unitaire |

## 🚀 Démarrage

### Démarrer le serveur de développement

```bash
python -m uvicorn main:app --reload --port 8000
```

**Sortie attendue :**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [XXXX]
INFO:     Application startup complete
```

### Accès aux services

- **API** : `http://localhost:8000`
- **Documentation interactive (Swagger UI)** : `http://localhost:8000/docs`
- **Documentation alternative (ReDoc)** : `http://localhost:8000/redoc`
- **Health Check** : `http://localhost:8000/health`

## 📁 Structure

```
backend/
├── main.py                      # Point d'entrée FastAPI
├── requirements.txt             # Dépendances Python
├── __init__.py
│
├── algorithms/                  # Implémentations d'algorithmes
│   ├── __init__.py
│   ├── dijkstra.py             # Plus court chemin (poids positifs)
│   ├── bellman_ford.py         # Plus court chemin (poids négatifs)
│   ├── bellman.py              # Variante Bellman
│   ├── kruskal.py              # Arbre couvrant minimal
│   ├── prim.py                 # Arbre couvrant minimal
│   ├── ford_fulkerson.py       # Flot maximal dans un réseau
│   ├── euler.py                # Chemin/Circuit Eulérien
│   ├── welsh_powell.py         # Coloration de graphe
│   ├── connected_components.py # Composantes connexes
│   └── strongly_connected_components.py  # Composantes fortement connexes
│
├── models/                      # Modèles de données (Pydantic)
│   ├── __init__.py
│   ├── graph.py                # Modèles: Graph, Edge, GraphRequest
│   ├── models.py               # Modèles génériques
│   └── mst_models.py           # Modèles spécifiques MST
│
├── routes/                      # Endpoints API (Routers FastAPI)
│   ├── __init__.py
│   ├── algorithms.py           # Routes: composantes, coloration
│   ├── graph_routes.py         # Routes: gestion graphes
│   ├── shortest_path_routes.py # Routes: chemins courts
│   ├── mst_routes.py           # Routes: arbres couvrants
│   └── ford_fulkerson_route.py # Routes: flot maximal
│
├── services/                    # Logique métier (services)
│   ├── graph_analyzer.py       # Analyse de graphes
│   ├── shortest_path_service.py # Service Dijkstra/Bellman-Ford
│   ├── mst_service.py          # Service Kruskal/Prim
│   └── ford_fulkerson_service.py # Service flot maximal
│
├── utils/                       # Fonctions utilitaires
│   ├── __init__.py
│   ├── utils.py                # Utilitaires génériques
│   ├── graph_utils.py          # Utilitaires spécifiques graphes
│   └── response_utils.py       # Format des réponses
│
└── tests/                       # Tests unitaires
    ├── __init__.py
    ├── README.md               # Documentation des tests
    ├── test_algorithms.py      # Tests d'algorithmes
    ├── test_mst.py            # Tests MST
    ├── test_euler.py          # Tests chemin Eulérien
    ├── test_welsh_powell.py   # Tests coloration
    ├── test_p1.html           # Résultats tests HTML
    └── test_p1_link           # Lien tests
```

## 🔌 Endpoints API

### Health Check

```http
GET /health
```

**Réponse :**
```json
{
  "status": "ok"
}
```

---

### 📊 Chemins les Plus Courts

#### Dijkstra

```http
POST /api/shortest-path/dijkstra
```

**Requête :**
```json
{
  "graph": {
    "nodes": ["A", "B", "C", "D"],
    "edges": [
      {"source": "A", "target": "B", "weight": 4},
      {"source": "B", "target": "C", "weight": 2},
      {"source": "A", "target": "C", "weight": 7},
      {"source": "C", "target": "D", "weight": 1}
    ],
    "directed": false
  },
  "start": "A"
}
```

**Réponse :**
```json
{
  "success": true,
  "algorithm": "dijkstra",
  "result": {
    "distances": {"A": 0, "B": 4, "C": 6, "D": 7},
    "predecessor": {"A": null, "B": "A", "C": "B", "D": "C"}
  },
  "steps": [
    {
      "iteration": 1,
      "visited": ["A"],
      "distances": {"A": 0}
    }
  ],
  "time_ms": 1.23
}
```

#### Bellman-Ford

```http
POST /api/shortest-path/bellman-ford
```

**Requête :** (format identique à Dijkstra)

---

### 🌳 Arbres Couvrants Minimaux

#### Kruskal

```http
POST /api/mst/kruskal
```

**Requête :**
```json
{
  "graph": {
    "nodes": ["A", "B", "C", "D"],
    "edges": [
      {"source": "A", "target": "B", "weight": 4},
      {"source": "B", "target": "C", "weight": 2},
      {"source": "A", "target": "C", "weight": 7},
      {"source": "C", "target": "D", "weight": 1}
    ],
    "directed": false
  }
}
```

**Réponse :**
```json
{
  "success": true,
  "algorithm": "kruskal",
  "result": {
    "mst_edges": [
      {"source": "C", "target": "D", "weight": 1},
      {"source": "B", "target": "C", "weight": 2},
      {"source": "A", "target": "B", "weight": 4}
    ],
    "total_weight": 7
  },
  "visualization": {
    "nodes": ["A", "B", "C", "D"],
    "edges": [...]
  },
  "time_ms": 0.85
}
```

#### Prim

```http
POST /api/mst/prim
```

**Requête :** (format identique à Kruskal)

---

### 🌊 Flot Maximal

#### Ford-Fulkerson

```http
POST /api/ford-fulkerson/max-flow
```

**Requête :**
```json
{
  "graph": {
    "nodes": ["S", "A", "B", "T"],
    "edges": [
      {"source": "S", "target": "A", "capacity": 10},
      {"source": "S", "target": "B", "capacity": 10},
      {"source": "A", "target": "T", "capacity": 10},
      {"source": "B", "target": "T", "capacity": 10}
    ],
    "directed": true
  },
  "source": "S",
  "sink": "T"
}
```

**Réponse :**
```json
{
  "success": true,
  "algorithm": "ford_fulkerson",
  "result": {
    "max_flow": 20,
    "flow_edges": [...]
  },
  "time_ms": 1.42
}
```

---

### 🔗 Analyse Structurelle

#### Composantes Connexes

```http
POST /api/graph/cc
```

**Requête :**
```json
{
  "graph": {
    "nodes": ["A", "B", "C", "D", "E"],
    "edges": [
      {"source": "A", "target": "B"},
      {"source": "B", "target": "C"},
      {"source": "D", "target": "E"}
    ],
    "directed": false
  }
}
```

**Réponse :**
```json
{
  "success": true,
  "algorithm": "cc",
  "result": {
    "components": [[A, B, C], [D, E]],
    "component_count": 2
  },
  "visualization": {...}
}
```

#### Composantes Fortement Connexes

```http
POST /api/graph/scc
```

**Requête :**
```json
{
  "graph": {
    "nodes": ["A", "B", "C", "D"],
    "edges": [
      {"source": "A", "target": "B"},
      {"source": "B", "target": "C"},
      {"source": "C", "target": "A"},
      {"source": "C", "target": "D"}
    ],
    "directed": true
  }
}
```

---

### 🔄 Chemins Eulériens

```http
POST /api/graph/euler
```

**Requête :**
```json
{
  "graph": {
    "nodes": ["A", "B", "C", "D"],
    "edges": [
      {"source": "A", "target": "B"},
      {"source": "B", "target": "C"},
      {"source": "C", "target": "D"},
      {"source": "D", "target": "A"}
    ],
    "directed": false
  }
}
```

---

### 🎨 Coloration Welsh-Powell

```http
POST /api/graph/welsh-powell
```

**Requête :**
```json
{
  "graph": {
    "nodes": ["A", "B", "C", "D"],
    "edges": [
      {"source": "A", "target": "B"},
      {"source": "B", "target": "C"},
      {"source": "C", "target": "D"},
      {"source": "D", "target": "A"},
      {"source": "A", "target": "C"}
    ],
    "directed": false
  }
}
```

**Réponse :**
```json
{
  "success": true,
  "algorithm": "welsh_powell",
  "result": {
    "coloring": {"A": 1, "B": 2, "C": 2, "D": 2},
    "chromatic_number": 2
  }
}
```

---

### 📈 Gestion des Graphes

#### Créer un graphe

```http
POST /api/graph/graphs
```

#### Récupérer un graphe

```http
GET /api/graph/graphs/{graph_id}
```

#### Modifier un graphe

```http
PUT /api/graph/graphs/{graph_id}
```

#### Supprimer un graphe

```http
DELETE /api/graph/graphs/{graph_id}
```

---

## 📊 Modèles de Données

### Graph

```python
class Graph(BaseModel):
    """Représentation complète d'un graphe."""
    nodes: list[str]          # Liste des sommets
    edges: list[Edge]         # Liste des arêtes
    directed: bool = False    # Graphe orienté ou non
```

### Edge

```python
class Edge(BaseModel):
    """Représentation d'une arête."""
    source: str               # Sommet source
    target: str               # Sommet cible
    weight: float = 1.0       # Poids de l'arête (optionnel)
    capacity: float = None    # Capacité (pour flot)
```

### GraphRequest

```python
class GraphRequest(BaseModel):
    """Requête pour créer/modifier un graphe."""
    nodes: list[str]
    edges: list[Edge]
    directed: bool = False
```

---

## 🧮 Algorithmes

### Classification par Complexité

| Algorithme | Complexité | Type |
|-----------|-----------|------|
| Dijkstra | O((V+E) log V) | Plus court chemin |
| Bellman-Ford | O(VE) | Plus court chemin |
| Kruskal | O(E log E) | MST |
| Prim | O((V+E) log V) | MST |
| Ford-Fulkerson | O(VE²) | Flot |
| Composantes Connexes | O(V+E) | Analyse |
| Welsh-Powell | O(V²) | Coloration |

### Détails Algorithmes

#### Dijkstra (`algorithms/dijkstra.py`)
- **Cas d'usage** : Trouver le plus court chemin dans un graphe à poids positifs
- **Entrée** : Graphe, nœud source
- **Sortie** : Distances et chemins vers tous les nœuds
- **Limitation** : Ne fonctionne pas avec poids négatifs

#### Bellman-Ford (`algorithms/bellman_ford.py`)
- **Cas d'usage** : Plus court chemin avec poids négatifs possibles
- **Entrée** : Graphe, nœud source
- **Sortie** : Distances et chemins
- **Avantage** : Détecte les cycles négatifs

#### Kruskal (`algorithms/kruskal.py`)
- **Cas d'usage** : Arbre couvrant minimal de poids minimal
- **Algorithme** : Greedy + Union-Find
- **Complexité** : O(E log E)

#### Prim (`algorithms/prim.py`)
- **Cas d'usage** : Arbre couvrant minimal
- **Algorithme** : Croissance depuis un nœud
- **Complexité** : O((V+E) log V) avec tas

#### Ford-Fulkerson (`algorithms/ford_fulkerson.py`)
- **Cas d'usage** : Flot maximal dans un réseau
- **Entrée** : Graphe orienté, source, destination
- **Sortie** : Flot maximal et distribution

#### Chemin Eulérien (`algorithms/euler.py`)
- **Cas d'usage** : Trouver un chemin passant par chaque arête exactement une fois
- **Conditions** : 0 ou 2 sommets de degré impair

#### Coloration Welsh-Powell (`algorithms/welsh_powell.py`)
- **Cas d'usage** : Colorer les sommets d'un graphe
- **Algorithme** : Greedy avec ordre décroissant de degré
- **Résultat** : Nombre chromatique et coloration

---

## 🧪 Tests

### Exécuter tous les tests

```bash
pytest tests/
```

### Exécuter un fichier de test spécifique

```bash
pytest tests/test_algorithms.py -v
```

### Exécuter un test précis

```bash
pytest tests/test_algorithms.py::test_dijkstra -v
```

### Générer un rapport de couverture

```bash
pytest tests/ --cov=backend --cov-report=html
```

### Fichiers de Test

| Fichier | Description |
|---------|-------------|
| `test_algorithms.py` | Tests des algorithmes génériques |
| `test_mst.py` | Tests Kruskal et Prim |
| `test_euler.py` | Tests chemin Eulérien |
| `test_welsh_powell.py` | Tests coloration |

---

## 🏗️ Architecture

### Flux de Requête

```
Client HTTP
    ↓
FastAPI Router (routes/*.py)
    ↓
Service (services/*.py)
    ↓
Algorithm (algorithms/*.py)
    ↓
Utilités (utils/*.py)
    ↓
Response Builder
    ↓
JSON Response
```

### Pile Technologique

```
┌─────────────────────────────────┐
│      Frontend (React/TypeScript) │
└─────────────────────────────────┘
            ↓ HTTP
┌─────────────────────────────────┐
│      FastAPI (main.py)          │
│   - CORS Middleware             │
│   - Routers                     │
└─────────────────────────────────┘
            ↓
┌─────────────────────────────────┐
│    Services & Algorithms        │
│   - Business Logic              │
│   - Computations                │
└─────────────────────────────────┘
            ↓
┌─────────────────────────────────┐
│    Utilities & Models           │
│   - Graph Structures            │
│   - Helper Functions            │
└─────────────────────────────────┘
```

### Patterns Utilisés

- **Router Pattern** : Séparation des endpoints par domaine
- **Service Pattern** : Logique métier isolée
- **Dependency Injection** : Via FastAPI
- **Validation** : Pydantic pour tous les modèles
- **Error Handling** : Réponses standardisées

---

## 🔐 Configuration CORS

Le serveur accepte actuellement les requêtes depuis :

```python
allow_origins=["http://localhost:5173"]  # Frontend Vite
```

**À modifier en production !**

---

## 📝 Conventions de Code

### Réponses API

Toutes les réponses suivent ce format :

```json
{
  "success": boolean,
  "algorithm": "algorithm_name",
  "result": { /* résultat spécifique */ },
  "visualization": { /* données pour visualisation */ },
  "time_ms": number,
  "error": "error message" // seulement si success=false
}
```

### Nommage des Fonctions

- Algorithmes : `snake_case` (ex: `dijkstra()`)
- Classes : `PascalCase` (ex: `GraphAnalyzer`)
- Constantes : `UPPER_SNAKE_CASE` (ex: `MAX_NODES`)

---

## 🐛 Debugging

### Activer le mode verbose

```bash
python -m uvicorn main:app --reload --log-level debug
```

### Voir les logs de FastAPI

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📚 Ressources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [Uvicorn Documentation](https://www.uvicorn.org)
- [Python 3 Documentation](https://docs.python.org/3)

---

## 🤝 Développement

### Ajouter un nouvel algorithme

1. Créer le fichier dans `algorithms/`
2. Implémenter la fonction principale
3. Ajouter les tests dans `tests/`
4. Créer un service dans `services/` si nécessaire
5. Ajouter un endpoint dans `routes/`
6. Tester avec Swagger UI

### Ajouter un nouvel endpoint

1. Créer/modifier un fichier dans `routes/`
2. Importer le service correspondant
3. Définir le modèle de requête avec Pydantic
4. Implémenter la fonction route
5. Tester via `http://localhost:8000/docs`

---

## 📋 Checklist Démarrage

- [ ] Python 3.9+ installé
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Serveur lancé (`python -m uvicorn main:app --reload`)
- [ ] Swagger UI accessible (`http://localhost:8000/docs`)
- [ ] Tests passant (`pytest tests/`)

---

**Version** : 1.0.0  
**Dernière mise à jour** : Mai 2026  
**Auteur** : Équipe TP Graphes
