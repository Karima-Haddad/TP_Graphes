from fastapi import FastAPI
from routes.ford_fulkerson_route import router

app = FastAPI(title="graph-platform")

app.include_router(router)
from backend.routes.mst_routes import router as mst_router

app = FastAPI(title="graph-platform")

app.include_router(mst_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}