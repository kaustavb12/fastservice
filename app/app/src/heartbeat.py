from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

heartbeatAPI = APIRouter()

@heartbeatAPI.get("/", summary="API Pulse Check", description="Health check of API")
async def check_health():
    return {"ok"}