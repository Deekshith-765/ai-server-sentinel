"""Dashboard: FastAPI Backend
Serves monitoring data and AI predictions via REST API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Intelligent Monitoring System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metrics_store = []
predictions_store = []


@app.get("/")
def root():
    return {"name": "Intelligent Monitoring System", "status": "running", "version": "1.0.0"}


@app.get("/api/health")
def health():
    return {"status": "healthy", "services": {"dev": "online", "sec": "online", "ops": "online"}}


@app.get("/api/metrics/latest")
def latest_metrics():
    if metrics_store:
        return metrics_store[-1]
    return {"message": "No metrics collected yet"}


@app.get("/api/metrics/history")
def metrics_history():
    return metrics_store[-50:] if len(metrics_store) > 50 else metrics_store


@app.post("/api/metrics/ingest")
def ingest_metrics(metrics: dict):
    metrics_store.append(metrics)
    return {"received": True, "total": len(metrics_store)}


@app.get("/api/predictions/latest")
def latest_prediction():
    if predictions_store:
        return predictions_store[-1]
    return {"message": "No predictions yet"}


@app.post("/api/predictions/ingest")
def ingest_prediction(prediction: dict):
    predictions_store.append(prediction)
    return {"received": True, "total": len(predictions_store)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
