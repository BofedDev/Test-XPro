from fastapi import FastAPI

from src.config import settings
from src.exceptions import register_exception_handlers
from src.categories.router import router as categories_router
from src.products.router import router as products_router

app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")
register_exception_handlers(app)


@app.get("/")
def root():
    return {"message": "Welcome to Shop API! Go to /docs for Swagger UI."}


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(categories_router)
app.include_router(products_router)
