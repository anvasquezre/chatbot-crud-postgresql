from fastapi import APIRouter, Depends, HTTPException
import json
from v1.routers import messages, sessions


from v1.utils.utils import has_access


# routes
PROTECTED = [Depends(has_access)]


router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
    responses={404: {"description": "Not found"}},
    dependencies=PROTECTED
)


router.include_router(messages.router)
router.include_router(sessions.router)

@router.get("/")
async def read_items():
    message = {"version":"API v1"}
    return json.dumps(message)