from fastapi import FastAPI
from app.routers import product
from app.routers import category
from app.database import Base, engine
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce Backend API",
    description="My first FastAPI e-commerce backend project",
    version="1.0.0"
)

app.include_router(product.router)
app.include_router(category.router)


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