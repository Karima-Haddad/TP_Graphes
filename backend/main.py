from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


try:
    from backend.routes.algorithms import router as algorithms_router
    from backend.routes.ford_fulkerson_route import router as ford_fulkerson_router
    from backend.routes.graph_routes import router as graph_router
    from backend.routes.mst_routes import router as mst_router
    from backend.routes.shortest_path_routes import router as shortest_path_router
except ModuleNotFoundError:  # pragma: no cover - compatibilite uvicorn depuis backend/
    from routes.algorithms import router as algorithms_router
    from routes.ford_fulkerson_route import router as ford_fulkerson_router
    from routes.graph_routes import router as graph_router
    from routes.mst_routes import router as mst_router
    from routes.shortest_path_routes import router as shortest_path_router


app = FastAPI(title="graph-platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(algorithms_router)
app.include_router(ford_fulkerson_router)
app.include_router(graph_router)
app.include_router(mst_router)
app.include_router(shortest_path_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
