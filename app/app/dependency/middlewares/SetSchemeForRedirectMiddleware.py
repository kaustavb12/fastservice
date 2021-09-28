from starlette.types import ASGIApp, Receive, Scope, Send

# Sets request protocol to "scheme" scope to be used if request needs to be forwarded to correct url
# Useful when api is behind application proxy, router or load balancer, ex. Traefik
# Ex. If request url does not end with '/' and is forwarded to url ending '/'
class SetSchemeForRedirectMiddleware:
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

        for x in scope["headers"]:
            if(x[0].decode("utf-8") == "x-forwarded-proto"):
                scope["scheme"] = x[1].decode("utf-8")

        await self.app(scope, receive, send)