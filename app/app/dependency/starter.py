from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from starlette_context import plugins, context
from starlette_context.middleware import RawContextMiddleware

from typing import Optional

from app.src.private_api import privateAPI
from app.src.public_api import publicAPI
from app.src.heartbeat import heartbeatAPI
from app.dependency.authentication import requires_auth
from app.dependency.middlewares.LogRequestCycleMiddleware import LogRequestCycleMiddleware
from app.dependency.app_logger.logger import configure_logging
from app.dependency.middlewares.AppendForwardPrefixMiddleware import AppendForwardPrefixMiddleware
from app.dependency.middlewares.SetSchemeForRedirectMiddleware import SetSchemeForRedirectMiddleware
from app.dependency.middlewares.ExceptionLogMiddleware import ExceptionLogMiddleware
from app.dependency.database import db
from . import config_settings as config

env_config: Optional[config.Settings] = None

def load_env_config():
    global env_config
    env_config = config.Settings()

def load_config_context():
    context["AUTH0_DOMAIN"] = env_config.auth0_domain
    context["AUTH0_API_IDENTIFIER"] = env_config.api_identifier
    algo_list = [i for i in env_config.algorithms.split(" ")]
    context["AUTH0_ALGORITHMS"] = algo_list
    context["SERVICE_NAME"] = env_config.service_name
    context["AUTH0_M2M_USER"] = env_config.m2m_user
    context["AUTH0_API_CLIENT_ID"] = env_config.api_client_id
    context["AUTH0_API_CLIENT_SECRET"] = env_config.api_client_secret

# To disable Swagger UI used docs_url=None
app = FastAPI(redoc_url=None)

def load_api_title_desc():
    app.title = env_config.service_name
    app.description = env_config.service_description

def add_api_middleware():
    origins_list = [i for i in env_config.origins.split(" ")]
    origins = origins_list

    app.add_middleware(
        AppendForwardPrefixMiddleware
    )

    app.add_middleware(
        SetSchemeForRedirectMiddleware
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        LogRequestCycleMiddleware
    )

    app.add_middleware(
        ExceptionLogMiddleware
    )

    app.add_middleware(
        RawContextMiddleware,
        plugins=(
            plugins.ApiKeyPlugin(),
            plugins.RequestIdPlugin(force_new_uuid=True),
            plugins.UserAgentPlugin()
        )
    )

@app.on_event("startup")
async def startup_event():
    load_env_config()
    configure_logging(env_config.logging_level, env_config.log_type)
    add_api_middleware()
    load_api_title_desc()
    await db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await db.disconnect()
    
app.include_router(
    privateAPI,
    prefix="/priv",
    tags=["protected"],
    dependencies=[Depends(load_config_context), Depends(requires_auth)]
)

app.include_router(
    publicAPI,
    prefix="/pub",
    tags=["public"],
    dependencies=[Depends(load_config_context)]
)

app.include_router(
    heartbeatAPI,
    prefix="/heartbeat",
    tags=["public", "heartbeat"]
)