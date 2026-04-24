from fastapi import FastAPI

app = FastAPI(title="Training Analyzer")

@app.get("/health")
def health():
    return {"status": "ok"}