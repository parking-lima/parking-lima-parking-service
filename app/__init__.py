from fastapi import FastAPI

app = FastAPI(
    title="Parking Lima - Parking Service",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "application": "Parking Lima",
        "service": "parking-service",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health/live")
def health_check():
    return {
        "status": "UP",
        "service": "parking-service"
    }

@app.get("/api/v1/districts")
def get_districts():
    return [
        {"id": 1, "name": "Miraflores"},
        {"id": 2, "name": "San Isidro"},
        {"id": 3, "name": "Santiago de Surco"}
    ]