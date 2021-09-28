from starlette.types import ASGIApp, Receive, Scope, Send
from app.dependency.app_logger.exception_logger import log_error
from starlette.requests import Request

# Catches all exceptions in the entire request life-cycle and logs it
class ExceptionLogMiddleware:
    def __init__(
        self, app: ASGIApp
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            request = Request(scope)
            try:
                await log_error("Exception Error", request, str(exc.reason.strerror))
            except:
                await log_error("Exception Error", request, str(exc))
            raise exc
