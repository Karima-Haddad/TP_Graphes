try:
    from backend.main import app
except ModuleNotFoundError:  # pragma: no cover - compatibilite uvicorn depuis backend/
    from main import app
