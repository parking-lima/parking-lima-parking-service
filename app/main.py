
from fastapi import FastAPI

from app.api.districts import router as districts_router

app = FastAPI(
    title="Parking Lima - Parking Service",
    description="Microservice for managing parking lots in Lima",
    version="0.1.0",
)

app.include_router(districts_router)


@app.get("/")
def root():
    return {
        "application": "Parking Lima",
        "service": "parking-service",
        "version": "0.1.0",
    }


@app.get("/health/live")
def health_check():
    return {
        "status": "UP",
        "service": "parking-service",
    }
