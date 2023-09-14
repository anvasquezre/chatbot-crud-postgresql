from fastapi import APIRouter, Depends, HTTPException
from typing import List
from v1.utils.utils import get_db_uri

from core.models.models import (
    Session as SessionModel,
    Message as MessageModel,
    SessionCreate,
)

from core.schemas.schemas import (
    Session as SessionSchema,
    Message as MessageSchema,
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.settings import settings

from sqlalchemy.orm import Session as SQLAlchemySession

router = APIRouter(prefix="/sessions",
    tags=["Sessions"],
    responses={404: {"description": "Not found"}},
)


# SQLAlchemy configuration for PostgreSQL

DATABASE_URL = get_db_uri()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=SessionModel)
def create_Session(session: SessionCreate, db: SQLAlchemySession = Depends(get_db)):
    try:
        db_session = SessionSchema(**session.model_dump())
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
@router.get("/{session_id}", response_model=SessionModel)
def read_Session(session_id: str, db: SQLAlchemySession = Depends(get_db)):
    
    try:
        db_session = db.query(SessionSchema).filter(SessionSchema.session_id == session_id).first()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db_session is None:
            raise HTTPException(status_code=404, detail="Session not found")
        return db_session
    

@router.put("/{session_id}", response_model=SessionModel)
def update_Session(session_id: str, Session: SessionCreate, db: SQLAlchemySession = Depends(get_db)):
    

    try:
        db_session = db.query(SessionSchema).filter(SessionSchema.session_id == session_id).first()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db_session is None:
            raise HTTPException(status_code=404, detail="Session not found")
        
    for key, value in Session.model_dump().items():
        setattr(db_session, key, value)
    try:
        db.commit()
        db.refresh(db_session)
        return db_session
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{session_id}", response_model=SessionModel)
def delete_Session(session_id: str, db: SQLAlchemySession = Depends(get_db)):
    
    try:
        db_session = db.query(SessionSchema).filter(SessionSchema.session_id == session_id).first()
    except HTTPException as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db_session is None:
            raise HTTPException(status_code=404, detail="Session not found")

    try:   
        db.delete(db_session)
        db.commit()
        return db_session
    except HTTPException as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

# List all Sessions
@router.get("/", response_model=List[SessionModel])
def list_Sessions(skip: int = 0, limit: int = 10, db: SQLAlchemySession = Depends(get_db)):
    try:
        sessions = db.query(SessionSchema).offset(skip).limit(limit).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    if not sessions:
        raise HTTPException(status_code=404, detail="Sessions not found")
    return sessions

# Endpoint to retrieve all messages from a single session
@router.get("/sessions/{session_id}/messages/", response_model=List[MessageModel])
def get_messages_for_session(session_id: str, db: SQLAlchemySession = Depends(get_db)):
    try:
        messages = db.query(MessageSchema).filter(MessageSchema.session_id == session_id).all()
    except HTTPException as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if not messages:
            raise HTTPException(status_code=404, detail="No messages found for this session")
        return messages
    