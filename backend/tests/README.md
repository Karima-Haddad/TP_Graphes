# Instructions de tests — backend

Ce fichier décrit la forme de l'input et de l'output pour les tests du service Ford-Fulkerson.

## Endpoint à tester

- Route : `POST /api/algorithms/ford-fulkerson`
- Payload JSON :
  - `graph` : objet décrivant le graphe
  - `params` : objet contenant la source et le puits

## Format attendu de l'input

```json
{
  "graph": {
    "directed": true,
    "weighted": true,
    "nodes": [
      { "id": "S", "label": "S", "x": 60, "y": 150 },
      { "id": "A", "label": "A", "x": 220, "y": 60 },
      { "id": "B", "label": "B", "x": 220, "y": 240 },
      { "id": "T", "label": "T", "x": 380, "y": 150 }
    ],
    "edges": [
      { "id": "e1", "source": "S", "target": "A", "weight": 10 },
      { "id": "e2", "source": "S", "target": "B", "weight": 10 },
      { "id": "e3", "source": "A", "target": "T", "weight": 10 },
      { "id": "e4", "source": "B", "target": "T", "weight": 10 },
      { "id": "e5", "source": "A", "target": "B", "weight": 1 }
    ]
  },
  "params": {
    "source": "S",
    "target": "T"
  }
}
```

### Notes sur l'input

- `directed` doit être `true` pour Ford-Fulkerson.
- `weighted` peut être `false` ; dans ce cas, les arêtes reçoivent une capacité par défaut de `1`.
- `nodes` doit contenir des objets avec au minimum : `id`.
- `edges` doit contenir des objets avec : `id`, `source`, `target` et éventuellement `weight`.
- `params.source` et `params.target` doivent correspondre à des `id` de nœuds existants.

## Format attendu de l'output

### Réponse de succès

La réponse renvoyée est une structure JSON avec ces champs principaux :

- `success`: boolean
- `algorithm`: `ford_fulkerson`
- `message`: texte
- `params`: mêmes paramètres envoyés
- `result`
  - `summary`
    - `max_flow`: valeur du flot maximum
    - `source`, `target`
    - `augmenting_paths`: nombre de chemins augmentants trouvés
  - `details`
    - `flow_on_edges`: détails des flots sur chaque arête
    - `augmenting_paths`: liste des chemins augmentants
- `visualization`
  - `result_graph`: graph final avec arêtes/nœuds mis en évidence
  - `steps`: étapes de l'algorithme pour la visualisation
- `meta`
  - `execution_time_ms`
  - `step_count`
  - `warnings`
- `error`: `null`

Exemple partiel :

```json
{
  "success": true,
  "algorithm": "ford_fulkerson",
  "message": "Exécution réussie",
  "params": { "source": "S", "target": "T" },
  "result": {
    "summary": {
      "max_flow": 20,
      "source": "S",
      "target": "T",
      "augmenting_paths": 2
    },
    "details": {
      "flow_on_edges": {
        "e1": { "flow": 10, "capacity": 10, "source": "S", "target": "A" },
        "e2": { "flow": 10, "capacity": 10, "source": "S", "target": "B" },
        "e3": { "flow": 10, "capacity": 10, "source": "A", "target": "T" },
        "e4": { "flow": 10, "capacity": 10, "source": "B", "target": "T" },
        "e5": { "flow": 0, "capacity": 1, "source": "A", "target": "B" }
      },
      "augmenting_paths": [
        { "iteration": 1, "path": ["S","A","T"], "flow": 10 },
        { "iteration": 2, "path": ["S","B","T"], "flow": 10 }
      ]
    }
  },
  "visualization": { ... },
  "meta": { "execution_time_ms": 12, "step_count": 5, "warnings": [] },
  "error": null
}
```

### Réponse d'erreur

Quand le graphe est invalide ou que les paramètres sont incorrects, l'API renvoie :

- `success`: `false`
- `result`: `null`
- `visualization`: `null`
- `error`: objet de validation

Exemple :

```json
{
  "success": false,
  "algorithm": "ford_fulkerson",
  "message": "Ford-Fulkerson s'applique à un graphe orienté...",
  "params": { "source": "S", "target": "T" },
  "result": null,
  "visualization": null,
  "meta": { "execution_time_ms": 0, "step_count": 0, "warnings": [] },
  "error": {
    "code": "INVALID_GRAPH_FOR_ALGORITHM",
    "type": "validation_error",
    "details": {}
  }
}
```

## Cas de test recommandés

1. Graphe valide orienté et pondéré : vérifier `max_flow` correct.
2. Graphe non orienté (`directed: false`) : vérifier erreur `INVALID_GRAPH_FOR_ALGORITHM`.
3. Arête de capacité négative ou nulle : vérifier erreur `INVALID_GRAPH_FOR_ALGORITHM`.
4. `source` absent ou `target` absent : vérifier erreur `NODE_NOT_FOUND`.
5. `source` égal à `target` : vérifier erreur `INVALID_PARAMS`.
6. Graphe non pondéré (`weighted: false`) : vérifier que les arêtes prennent la capacité par défaut `1`.
7. Normalisation des nœuds/arêtes : envoyer un graphe avec des nœuds sans `label` et des arêtes sans `label`, et vérifier que l'API répond sans erreur.

## Comment écrire un test

- Crée un fichier de test dans ce dossier, par exemple `test_ford_fulkerson.py`.
- Utilise `pytest` ou le framework de test installé.
- Pour les tests d'API, tu peux appeler la fonction de service `run(graph, params)` ou la route FastAPI directement.
- Vérifie à la fois le code HTTP (si tu tests l'API) et la structure JSON retournée.
- Contrôle les champs `success`, `result.summary.max_flow`, `error.code`, et la présence de `visualization.steps`.

## Exécution

Si `pytest` est installé, lance les tests depuis le dossier `backend` :

```bash
cd backend
pytest
```

Si `pytest` n'est pas installé, ajoute-le dans `backend/requirements.txt` :

```text
pytest
```
