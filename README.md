## 📊 GraphLab — Plateforme d’expérimentation des algorithmes de graphes
- **👥 Équipe**
- Bayrem Kahna
- Emna Kallel
- Karima Hadadd
- Maha Tlili
- Mayssa Chikh Ali
- Melek Kammoun
- Nadine Ben Makhlouf
- Nour Khelifi
- Yossr Galai
- Zayd Hefyen


## 🎯 Objectif du projet

GraphLab est une application interactive permettant de créer, visualiser et analyser des graphes, ainsi que d’exécuter plusieurs algorithmes classiques avec affichage des résultats et des étapes.

### Algorithmes Implémentés

- **Chemins Les Plus Courts**
  - 🔴 Algorithme de Bellman-Ford : chemin optimal avec poids négatifs
  - 🟠 Algorithme de Bellman : variante du calcul de plus court chemin
  - 🟢 Algorithme de Dijkstra : recherche rapide du chemin minimal

- **Arbres Couvrants Minimaux (MST)**
  - 🔷 Algorithme de Kruskal : sélection d’arêtes croissantes
  - 🔷 Algorithme de Prim : construction progressive de l’arbre

- **Flot Maximum**
  - 🌊 Algorithme de Ford-Fulkerson : calcul du flot maximal

- **Analyse Structurelle**
  - 🔗 Composantes Connexes : sous-graphes connectés
  - 🔗 Composantes Fortement Connexes : cycles en graphe orienté
  - 🔍 Test de connexité : vérifie si le graphe est connexe
  - ⚖️ Graphe biparti : vérification par coloration en 2 couleurs
  - 🔁 Détection de cycles : présence ou absence de cycles
  - 🌳 Vérification d’arbre : graphe connexe sans cycle

- **Circuits et Coloration**
  - 🔄 Chemin / Circuit Eulérien : passage unique par chaque arête
  - 🎨 Welsh-Powell : coloration des sommets

### Interface Utilisateur

- ✏️ Création interactive de graphes (sommets et arêtes)
- 📈 Visualisation dynamique des graphes
- ⚙️ Configuration flexible des paramètres
- 📊 Affichage détaillé des résultats
- 🎛️ Support des graphes orientés et non-orientés
- 💾 Gestion persistante des données



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


## 🚀 Démarrage Rapide

### Prérequis

- **Node.js** 18+ (pour le frontend)
- **Python** 3.9+ (pour le backend)
- **pip** (gestionnaire de paquets Python)

### Installation

```bash
# 1. Cloner le projet
cd TP_Graphes

# 2. Installer les dépendances du backend
cd backend
pip install -r requirements.txt

# 3. Installer les dépendances du frontend
cd ../frontend
npm install
```

### Lancer l'Application

#### Terminal 1 - Backend (FastAPI)
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```
Le backend sera accessible sur `http://localhost:8000`

#### Terminal 2 - Frontend (React + Vite)
```bash
cd frontend
npm run dev
```
L'application sera accessible sur `http://localhost:5173`

### Build pour Production

**Frontend:**
```bash
cd frontend
npm run build
```

**Backend:** Voir la documentation de déploiement FastAPI

## 📁 Structure du Projet

```
TP_Graphes/
├── backend/                          # API Python (FastAPI)
│   ├── main.py                       # Point d'entrée de l'application
│   ├── requirements.txt              # Dépendances Python
│   ├── algorithms/                   # Implémentations des algorithmes
│   │   ├── dijkstra.py
│   │   ├── bellman_ford.py
│   │   ├── kruskal.py
│   │   ├── prim.py
│   │   ├── ford_fulkerson.py
│   │   ├── euler.py
│   │   ├── welsh_powell.py
│   │   └── connected_components.py
│   ├── models/                       # Modèles de données (Pydantic)
│   │   ├── graph.py                  # Modèles Graph et Edge
│   │   └── mst_models.py
│   ├── routes/                       # Endpoints API
│   │   ├── graph_routes.py           # CRUD graphes
│   │   ├── shortest_path_routes.py   # Endpoints chemins courts
│   │   ├── mst_routes.py             # Endpoints MST
│   │   └── ford_fulkerson_route.py   # Endpoints flot
│   ├── services/                     # Logique métier
│   │   ├── graph_analyzer.py
│   │   ├── shortest_path_service.py
│   │   ├── mst_service.py
│   │   └── ford_fulkerson_service.py
│   └── tests/                        # Tests unitaires
│       ├── test_algorithms.py
│       ├── test_mst.py
│       └── test_welsh_powell.py
│
├── frontend/                         # Application React/TypeScript
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts               # Configuration Vite
│   ├── tsconfig.json
│   ├── src/
│   │   ├── main.tsx                 # Point d'entrée
│   │   ├── App.tsx                  # Composant racine
│   │   ├── pages/                   # Pages principales
│   │   │   ├── GraphPage.tsx        # Visualisation des graphes
│   │   │   ├── CréationGraphe.tsx   # Création de graphes
│   │   │   └── AlgorithmPage.tsx    # Exécution des algorithmes
│   │   ├── components/              # Composants réutilisables
│   │   │   ├── VisualisationGraphe.tsx
│   │   │   ├── PannelConfigGraphe.tsx
│   │   │   ├── AlgorithmSidebar.tsx
│   │   │   └── AlgorithmResultCard.tsx
│   │   ├── services/                # Appels API
│   │   │   ├── executionApi.ts
│   │   │   └── graphPropertiesApi.ts
│   │   ├── types/                   # Types TypeScript
│   │   │   ├── graph.types.ts
│   │   │   └── algorithm.types.ts
│   │   └── utils/                   # Fonctions utilitaires
│   └── public/                      # Ressources statiques
│
└── data/                            # Données et fichiers
```

## 🔌 Architecture API

### Endpoints Principaux

**Graphes**
- `POST /graphs` - Créer un nouveau graphe
- `GET /graphs/{id}` - Récupérer un graphe
- `PUT /graphs/{id}` - Modifier un graphe
- `DELETE /graphs/{id}` - Supprimer un graphe

**Chemins les Plus Courts**
- `POST /dijkstra` - Calculer avec Dijkstra
- `POST /bellman-ford` - Calculer avec Bellman-Ford

**Arbres Couvrants Minimaux**
- `POST /mst/kruskal` - MST avec Kruskal
- `POST /mst/prim` - MST avec Prim

**Flot Maximum**
- `POST /ford-fulkerson` - Calculer le flot maximal

**Analyse Structurelle**
- `POST /connected-components` - Composantes connexes
- `POST /strongly-connected-components` - Composantes fortement connexes
- `POST /euler` - Chemin Eulérien
- `POST /welsh-powell` - Coloration de graphe

## 🛠️ Technologies Utilisées

### Backend
- **FastAPI** - Framework web moderne et performant
- **Pydantic** - Validation de données
- **Uvicorn** - Serveur ASGI
- **Python 3.9+**

### Frontend
- **React 19** - Bibliothèque d'interface utilisateur
- **TypeScript** - Typage statique pour JavaScript
- **React Router** - Navigation entre pages
- **Vite** - Bundler ultrarapide
- **ESLint** - Linter pour la qualité du code

### Infrastructure
- **CORS** - Partage des ressources entre domaines
- **REST API** - Architecture des services web

## 💻 Développement

### Tester le Backend

```bash
cd backend
pytest tests/
```

### Linter le Frontend

```bash
cd frontend
npm run lint
```

### Architecture du Flux Données

```
Frontend (React/TypeScript)
        ↓
    HTTP Requests
        ↓
Backend API (FastAPI)
        ↓
Algorithmes (Python)
        ↓
    HTTP Responses
        ↓
Frontend (Affichage)
```

## 📝 Format des Requêtes

### Exemple : Créer et analyser un graphe

```json
{
  "nodes": ["A", "B", "C", "D"],
  "edges": [
    {"source": "A", "target": "B", "weight": 4},
    {"source": "B", "target": "C", "weight": 2},
    {"source": "A", "target": "C", "weight": 7},
    {"source": "C", "target": "D", "weight": 1}
  ],
  "directed": false
}
```


## 🤝 Contribution

Ce projet est un travail pédagogique. Les contributions sont bienvenues pour :
- Améliorer les performances des algorithmes
- Ajouter de nouveaux algorithmes
- Améliorer l'interface utilisateur
- Corriger les bugs

