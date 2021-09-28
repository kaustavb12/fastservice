from starlette.types import ASGIApp, Receive, Scope, Send
from app.dependency.app_logger.logger import log
import time

# Logs incoming request path and turn around time of request at end of request life-cycle.
class LogRequestCycleMiddleware:
    def __init__(
        self, app: ASGIApp
    ) -> None:
        self.app = app

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        if scope["type"] not in ("http"):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        path = scope["path"]

        if(path != "/heartbeat/"):
            start_time = time.time()
            log.info("start request path=%s", path)
    
        await self.app(scope, receive, send)

        if(path != "/heartbeat/"):
            process_time = (time.time() - start_time)*1000
            formatted_process_time = '{0:.2f}ms'.format(process_time)
            log.info("end request tat=%s", formatted_process_time)
