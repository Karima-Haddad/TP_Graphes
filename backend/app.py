from fastapi import FastAPI

app = FastAPI(title="graph-platform")


@app.get("/health")
def health_check():
    return {"status": "ok"}
