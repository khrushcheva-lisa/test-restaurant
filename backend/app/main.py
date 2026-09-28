from fastapi import FastAPI

from app.api.dishes import router as dishes_router
from app.api.clients import router as clients_router


app = FastAPI(
    title="Restaurant API"
)


app.include_router(dishes_router)
app.include_router(clients_router)


@app.get("/")
def root():
    return {
        "message": "API is working"
    }