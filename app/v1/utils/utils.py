from typing import Optional
import jwt
from jwt.exceptions import InvalidSignatureError

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.settings import settings

security = HTTPBearer()
API_KEY = settings.api.API_KEY
ALG = settings.api.ALG

async def has_access(credentials: HTTPAuthorizationCredentials= Depends(security)):
    """
        Function that is used to validate the token in the case that it requires it
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token,API_KEY,algorithms=[ALG],verify=True)
    except InvalidSignatureError as e:  # catches any exception
        raise HTTPException(
            status_code=401,
            detail=str(e))
        
        
def get_db_uri(POSTGRES_USER : Optional[str] = settings.db.POSTGRES_USER,
               POSTGRES_PASSWORD:Optional[str] = settings.db.POSTGRES_PASSWORD,
               POSTGRES_HOST:Optional[str] = settings.db.POSTGRES_HOST,
               POSTGRES_PORT:Optional[str] = settings.db.POSTGRES_PORT,
               POSTGRES_DB:Optional[str] = settings.db.POSTGRES_DB
               ) -> str: 
    DB_URI:str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    return DB_URI