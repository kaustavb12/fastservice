from fastapi.testclient import TestClient
from starlette_context import context, plugins
from starlette_context.middleware import RawContextMiddleware

from app.main import app
from app.dependency import starter
from app.dependency import authentication
from app.dependency.middlewares.LogRequestCycleMiddleware import LogRequestCycleMiddleware
import app.dependency.config_settings as config
from app.src.public_api import get_db
from databases import Database

import pytest
from httpx import AsyncClient

app.add_middleware(
    LogRequestCycleMiddleware
)

app.add_middleware(
    RawContextMiddleware,
    plugins=(
        plugins.ApiKeyPlugin(),
        plugins.RequestIdPlugin(force_new_uuid=True),
        plugins.UserAgentPlugin()
    )
)

client = TestClient(app)

def load_config_context_override():
    context["AUTH0_DOMAIN"] = "domain.example.com"
    context["AUTH0_API_IDENTIFIER"] = "api.example.com"
    context["AUTH0_ALGORITHMS"] = "RSA256"
    context["SERVICE_NAME"] = "Testing Service"

def requires_auth_override():
    context["USER_ID"] = "auth0|123456789012345678901234"

def requires_scope_override():
    return True

def generateURL(username: str, password: str, host: str, database: str):
    return 'postgres://' + username + ":" + password + "@" + host + "/" + database

async def get_db_override():
    env_config = config.Settings()
    username = env_config.fastservice_postgres_user
    password = env_config.fastservice_postgres_passwd
    host = env_config.fastservice_postgres_host
    database = env_config.fastservice_postgres_db
    url = generateURL(username, password, host, database)
    db = Database(url=url, force_rollback=True)
    await db.connect()
    return db

app.dependency_overrides[starter.load_config_context] = load_config_context_override
app.dependency_overrides[authentication.requires_auth] = requires_auth_override
app.dependency_overrides[authentication.requires_scope] = requires_scope_override
app.dependency_overrides[get_db] = get_db_override

def test_private_api():
    response = client.get("/priv/private_api/", headers={"User-Agent": "test-user-agent"})
    assert response.status_code == 200
    assert response.json() == {
        "Hello User": "auth0|123456789012345678901234"
    }

@pytest.mark.asyncio
async def test_public_api():
    # response = client.get("/pub", headers={"User-Agent": "test-user-agent"})
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(url="/pub/public_api/", headers={"User-Agent": "test-user-agent"})
    assert response.status_code == 200
    assert response.json() == {
        "Hello": "Visitor # 1"
    }