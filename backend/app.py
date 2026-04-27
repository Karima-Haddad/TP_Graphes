from fastapi import FastAPI
from routes.shortest_path_routes import router as shortest_path_router

from routes.ford_fulkerson_route import router
from backend.routes.mst_routes import router as mst_router

app = FastAPI(title="graph-platform")

app.include_router(router)
app.include_router(mst_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(shortest_path_router)
    return {"status": "ok"}
