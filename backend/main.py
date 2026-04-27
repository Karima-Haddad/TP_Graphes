from fastapi import FastAPI

try:
    from backend.routes.algorithms import router as algorithms_router
except ModuleNotFoundError:  # pragma: no cover - compatibilite uvicorn depuis backend/
    from routes.algorithms import router as algorithms_router


app = FastAPI(title="graph-platform")
app.include_router(algorithms_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
