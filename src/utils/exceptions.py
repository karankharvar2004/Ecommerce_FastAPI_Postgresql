from fastapi import (
    Request,
    status
)

from fastapi.responses import JSONResponse

from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException

from src.utils.response import ResponseHandler


class ExceptionHandler:

    @classmethod
    async def http_exception_handler(
        cls,
        request: Request,
        exc: HTTPException
    ):

        return JSONResponse(
            status_code=exc.status_code,
            content=ResponseHandler.error(
                message=exc.detail
            )
        )


    @classmethod
    async def validation_exception_handler(
        cls,
        request: Request,
        exc: RequestValidationError
    ):

        validation_errors = []

        for error in exc.errors():

            validation_errors.append({
                "field": (
                    ".".join(
                        map(str, error["loc"])
                    )
                ),
                "message": error["msg"]
            })

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ResponseHandler.error(
                message="Validation Error",
                errors=validation_errors
            )
        )


    @classmethod
    async def internal_server_exception_handler(
        cls,
        request: Request,
        exc: Exception
    ):

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ResponseHandler.error(
                message="Internal Server Error"
            )
        )