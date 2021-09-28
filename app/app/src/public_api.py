from starlette_context import context
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from app.dependency.app_logger.logger import log
from app.dependency.database import db as dat

publicAPI = APIRouter()

def get_db():
    return dat

# Public API. No access bearer token needed to access public APIs
@publicAPI.get("/public_api/", summary="Public API demo", description="Sample pubilc API")
async def public_api(db = Depends(get_db)):
    log.debug("This is Public API")
    # Request id available in context through out request life cycle
    reqid = context.get("X-Request-ID")

    query1 = "SELECT count FROM counter"
    query2 = "UPDATE counter SET count = count + 1"
    query3 = "INSERT INTO insert_entrylog (request_id) VALUES (:id)"

    result = await db.fetch_one(query=query1)    

    async with db.transaction():
        await db.execute(query=query2)
        await db.execute(query=query3, values={"id": reqid})

    count = result["count"]
    
    return {"Hello": "Visitor # "+str(count)}