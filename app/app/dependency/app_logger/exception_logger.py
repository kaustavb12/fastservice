from starlette.requests import Request
from app.dependency.app_logger.logger import log

# Logs all errors from error_handler.py
def log_error(error_type: str, request: Request, error: str):
    err_url = str(request.url.path)
    if(len(request.query_params) != 0):
        err_url += "?" + str(request.query_params)
    log.error(error_type + "(" + err_url + ") : " + error)