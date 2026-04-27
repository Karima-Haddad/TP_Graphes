from fastapi import FastAPI
from routes.shortest_path_routes import router as shortest_path_router


app = FastAPI(title="graph-platform")


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(shortest_path_router)