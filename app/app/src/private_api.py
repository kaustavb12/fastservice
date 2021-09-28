from starlette_context import context
from fastapi import APIRouter, status, Security
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from pydantic import BaseModel
from app.dependency.authentication import requires_scope, requires_permission, requires_m2m_user
from app.dependency.app_logger.logger import log
from app.dependency.database import db as dat

privateAPI = APIRouter()

def get_db():
    return dat

# Private API. Valid access bearer token needed to access private APIs
@privateAPI.get("/private_api/", summary="Private API demo", description="Sample private API")
async def private_api():
    log.debug("This is Private API")

    # User id available in context for all private APIs
    user_id = context.get("USER_ID")

    return {"Hello User": user_id}



# M2M Private API. Valid m2m access bearer token needed to access m2m private APIs
@privateAPI.get("/m2m_api/{id}", dependencies=[Security(requires_m2m_user)], summary="M2M API demo", description="Sample m2m API")
async def m2m_api(id: int):
    if id == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item Id", headers={"X-Error" : "Invalid Id"})
    log.debug("This is M2M API")

    # User id available in context for all private APIs
    user_id = context.get("USER_ID")

    return {"This is Message # ": id}



# Permissioned Private API. Valid access bearer token with permissions given in scopes below needed to access premissioned private APIs
@privateAPI.get("/permissioned_api/", dependencies=[Security(requires_permission, scopes=['read:messages'])], summary="Permissioned API demo", description="Sample permissioned API")
async def permissioned_api():
    log.debug("This is Permissioned API")

    # User id available in context for all private APIs
    user_id = context.get("USER_ID")

    return {"Hello User": user_id}


# Scoped Private API. Valid access bearer token with scopes given in scopes below needed to access scoped private APIs
@privateAPI.get("/scoped_api/", dependencies=[Security(requires_scope, scopes=['message'])], summary="Scoped API demo", description="Sample scoped API")
async def scoped_api():
    log.debug("This is Scoped API")

    # User id available in context for all private APIs
    user_id = context.get("USER_ID")

    return {"Hello User": user_id}