from fastapi import FastAPI

from app.api.dishes import router as dishes_router
from app.api.clients import router as clients_router
from app.api.dishes_categories import router as dishes_categories_router
from app.api.ingredients import router as ingredients_router

app = FastAPI(
    title="Restaurant API"
)


app.include_router(dishes_router)
app.include_router(clients_router)
app.include_router(dishes_categories_router)
app.include_router(ingredients_router)


@app.get("/")
def root():
    return {
        "message": "API is working"
    }