from fastapi import FastAPI

from src.urls.v1.api import router

from fastapi.exceptions import (
    RequestValidationError
)

from starlette.exceptions import HTTPException

from src.utils.exceptions import (
    ExceptionHandler
)


app = FastAPI(
    title="Ecommerce Company Architecture API"
)

app.add_exception_handler(
    HTTPException,
    ExceptionHandler.http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    ExceptionHandler.validation_exception_handler
)

app.add_exception_handler(
    Exception,
    ExceptionHandler.internal_server_exception_handler
)


@app.get("/")
async def home():

    return {
        "message": "Ecommerce Backend Running Successfully"
    }


app.include_router(router)