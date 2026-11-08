import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

from app.core.validation import translate_validation_error

from app.api.auth_router import router as auth_router
from app.api.dishes_router import router as dishes_router
from app.api.clients_router import router as clients_router
from app.api.dishes_categories_router import router as dishes_categories_router
from app.api.ingredients_router import router as ingredients_router
from app.api.dishes_ingredients_router import router as dishes_ingredients_router

app = FastAPI(title="Restaurant API", version="1.0.0", description="REST API информационной системы ресторана")

app.include_router(auth_router)
app.include_router(dishes_router)
app.include_router(clients_router)
app.include_router(dishes_categories_router)
app.include_router(ingredients_router)
app.include_router(dishes_ingredients_router)

@app.get("/", tags=["System"])
def root():
    return {"message": "API is working"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    details = []

    for error in exc.errors():
        location = error.get("loc", ())
        field = location[-1] if location else "unknown"

        details.append({
            "field": field,
            "message": translate_validation_error(error)
        })

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Ошибка валидации входных данных",
            "details": details,
            "path": request.url.path
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={
        "success": False,
        "error": exc.detail,
        "path": request.url.path,
    }, headers=exc.headers)


logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def unexpected_exception_handler(request: Request, exc: Exception):
    logger.exception("Непредвиденная ошибка при обработке запроса: %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Внутренняя ошибка сервера",
            "path": request.url.path,
        },
    )
