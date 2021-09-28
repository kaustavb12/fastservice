from .starter import app
from fastapi import status
from fastapi.exceptions import HTTPException,RequestValidationError
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.dependency.app_logger.exception_logger import log_error

class Error(BaseModel):
    error: str

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    log_error("Request Data Validation Error", request, str(exc))
    error = Error(error = str(exc))
    return JSONResponse(content=jsonable_encoder(error), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    log_error("HTTPException Error", request, str(exc.detail))
    error = Error(error = str(exc.detail))
    return JSONResponse(content=jsonable_encoder(error), status_code=exc.status_code, headers=exc.headers)

@app.exception_handler(StarletteHTTPException)
def starlette_http_exception_handler(request, exc):
    log_error("StarletteHTTPException Error", request, str(exc.detail))
    error = Error(error = str(exc.detail))
    return JSONResponse(content=jsonable_encoder(error), status_code=exc.status_code)

@app.exception_handler(Exception)
def exception_handler(request, exc):
    error = Error(error = "Internal Server Error")
    return JSONResponse(content=jsonable_encoder(error), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)