"""
Routes FastAPI — Prim & Kruskal
Préfixe : /api/mst
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.models.mst_models import MSTRequest
from backend.services.mst_service import execute_mst

router = APIRouter(prefix="/api/mst", tags=["MST"])


@router.post(
    "/run",
    summary="Exécuter Prim ou Kruskal",
    description=(
        "Lance l'algorithme Prim ou Kruskal sur le graphe fourni. "
        "Retourne le résultat + les étapes de visualisation."
    ),
)
async def run_mst(body: MSTRequest) -> JSONResponse:
    """
    Corps de la requête :
    ```json
    {
      "algorithm": "prim",          // ou "kruskal"
      "graph": { ... },             // structure standard GraphLab
      "params": { "start_node": "A" }  // optionnel pour prim, vide pour kruskal
    }
    ```
    """
    graph_dict = body.graph.model_dump()
    result = execute_mst(
        algorithm=body.algorithm,
        graph_dict=graph_dict,
        params=body.params,
    )
    status_code = 200 if result.get("success") else 422
    return JSONResponse(content=result, status_code=status_code)


@router.post(
    "/prim",
    summary="Exécuter Prim directement",
)
async def run_prim_direct(body: MSTRequest) -> JSONResponse:
    """Raccourci — force l'algorithme à 'prim' peu importe le champ algorithm."""
    graph_dict = body.graph.model_dump()
    result = execute_mst("prim", graph_dict, body.params)
    status_code = 200 if result.get("success") else 422
    return JSONResponse(content=result, status_code=status_code)


@router.post(
    "/kruskal",
    summary="Exécuter Kruskal directement",
)
async def run_kruskal_direct(body: MSTRequest) -> JSONResponse:
    """Raccourci — force l'algorithme à 'kruskal' peu importe le champ algorithm."""
    graph_dict = body.graph.model_dump()
    result = execute_mst("kruskal", graph_dict, body.params)
    status_code = 200 if result.get("success") else 422
    return JSONResponse(content=result, status_code=status_code)