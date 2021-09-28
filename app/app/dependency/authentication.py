from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes
from urllib.request import urlopen
import json
from jose import jwt
from starlette_context import context

class OAuth2UnauthenticatedError(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status.HTTP_401_UNAUTHORIZED, **kwargs)

class OAuth2UnauthorizedError(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status.HTTP_403_FORBIDDEN, **kwargs)

class OAuth2HTTPBearer(HTTPBearer):
    async def __call__(self, request: Request):
        return await super().__call__(request)

def requires_auth(creds: HTTPAuthorizationCredentials = Depends(OAuth2HTTPBearer())):
    """Determines if the access token is valid
    """

    AUTH0_DOMAIN = context["AUTH0_DOMAIN"]
    ALGORITHMS = context["AUTH0_ALGORITHMS"]
    API_IDENTIFIER = context["AUTH0_API_IDENTIFIER"]

    SERVICE_NAME = context["SERVICE_NAME"]

    token = creds.credentials
    
    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise OAuth2UnauthenticatedError(detail="invalid_header : Invalid JWT Access Token", headers={'WWW-Authenticate': f'Bearer realm="{SERVICE_NAME}"'})
    if unverified_header["alg"] not in ALGORITHMS:
        raise OAuth2UnauthenticatedError(detail="invalid_header : JWT Access Token Signed Using Invalid Algorithm", headers={'WWW-Authenticate': f'Bearer realm="{SERVICE_NAME}"'})
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_IDENTIFIER,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
        except jwt.ExpiredSignatureError:
            raise OAuth2UnauthenticatedError(detail="token_expired : Token is Expired", headers={'WWW-Authenticate': f'Bearer realm="{SERVICE_NAME}"'})
        except jwt.JWTClaimsError:
            raise OAuth2UnauthenticatedError(detail="invalid_claims : Incorrect Claims, Please Check the Audience and Issuer", headers={'WWW-Authenticate': f'Bearer realm="{SERVICE_NAME}"'})
        except Exception:
            raise OAuth2UnauthenticatedError(detail="invalid_header : Unable to Parse JWT Access Token", headers={'WWW-Authenticate': f'Bearer realm="{SERVICE_NAME}"'})
        context["USER_ID"] = payload["sub"]
        return None
    raise OAuth2UnauthenticatedError(detail="invalid_header : Unable to Find Appropriate Key", headers={'WWW-Authenticate': f'Bearer realm="{SERVICE_NAME}"'})


def requires_m2m_user(creds: HTTPAuthorizationCredentials = Depends(OAuth2HTTPBearer())):
    """Determines if the access token is from authorized m2m user
    """

    SERVICE_NAME = context["SERVICE_NAME"]
    M2M_USER = context["AUTH0_M2M_USER"]

    token = creds.credentials
    unverified_claims = jwt.get_unverified_claims(token)
    if not unverified_claims.get("sub"):
        raise OAuth2UnauthorizedError(detail="Unauthorized : Subject missing from JWT Access Token", headers={'WWW-Authenticate': f'Bearer realm="{SERVICE_NAME}"'})

    sub_splits = unverified_claims.get("sub").split("@")

    if M2M_USER not in sub_splits:
        raise OAuth2UnauthorizedError(detail="Unauthorized : User Not Authorized to Access This Resource", headers={'WWW-Authenticate': f'Bearer realm="{SERVICE_NAME}"'})


def requires_scope(security_scopes: SecurityScopes, creds: HTTPAuthorizationCredentials = Depends(OAuth2HTTPBearer())):
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """

    SERVICE_NAME = context["SERVICE_NAME"]

    token = creds.credentials
    unverified_claims = jwt.get_unverified_claims(token)
    if not unverified_claims.get("scope"):
        raise OAuth2UnauthorizedError(detail="Unauthorized : Scope missing from JWT Access Token", headers={'WWW-Authenticate': f'Bearer realm="{SERVICE_NAME}" scope="{security_scopes.scope_str}"'})
    token_scopes = unverified_claims["scope"].split()
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise OAuth2UnauthorizedError(detail="Unauthorized : User Not Authorized to Access This Resource", headers={'WWW-Authenticate': f'Bearer realm="{SERVICE_NAME}" scope="{security_scopes.scope_str}"'})


def requires_permission(security_permissions: SecurityScopes, creds: HTTPAuthorizationCredentials = Depends(OAuth2HTTPBearer())):
    """Determines if the required permission is present in the access token
    Args:
        requires_permission (str): The permission required to access the resource
    """

    SERVICE_NAME = context["SERVICE_NAME"]

    token = creds.credentials
    unverified_claims = jwt.get_unverified_claims(token)
    if not unverified_claims.get("permissions"):
        raise OAuth2UnauthorizedError(detail="Unauthorized : Permissions missing from JWT Access Token", headers={'WWW-Authenticate': f'Bearer realm="{SERVICE_NAME}" permission="{security_permissions.scope_str}"'})
    token_permissions = unverified_claims["permissions"]
    for permission in security_permissions.scopes:
        if permission not in token_permissions:
            raise OAuth2UnauthorizedError(detail="Unauthorized : User Not Authorized to Access This Resource", headers={'WWW-Authenticate': f'Bearer realm="{SERVICE_NAME}" permission="{security_permissions.scope_str}"'})