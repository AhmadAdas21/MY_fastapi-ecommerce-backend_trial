from fastapi import FastAPI
from app.routers import product

app = FastAPI(
    title="E-commerce Backend API",
    description="My first FastAPI e-commerce backend project",
    version="1.0.0"
)

app.include_router(product.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to E-commerce Backend API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }