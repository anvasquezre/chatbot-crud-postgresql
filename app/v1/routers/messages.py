from fastapi import APIRouter, Depends, HTTPException
from typing import List

from core.models.models import (
    Message as MessageModel,
    MessageCreate,
)

from core.schemas.schemas import (
    Message as MessageSchema,
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.settings import settings

from sqlalchemy.orm import Session as SQLAlchemySession

from v1.utils.utils import get_db_uri

import uuid

router = APIRouter(prefix="/messages",
    tags=["Messages"],
    responses={404: {"description": "Not found"}}
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


@router.post("/", response_model=MessageModel)
def create_message(message: MessageCreate, db: SQLAlchemySession = Depends(get_db)):
    try:
        id = uuid.uuid4()
        db_message = MessageSchema(**message.model_dump())
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
@router.get("/{message_id}", response_model=MessageModel)
def read_message(message_id: str, db: SQLAlchemySession = Depends(get_db)):
    
    try:
        db_message = db.query(MessageSchema).filter(MessageSchema.message_id == message_id).first()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db_message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        return db_message
    

@router.put("/{message_id}", response_model=MessageModel)
def update_message(message_id: str, message: MessageCreate, db: SQLAlchemySession = Depends(get_db)):
    

    try:
        db_message = db.query(MessageSchema).filter(MessageSchema.message_id == message_id).first()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db_message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        
    for key, value in message.model_dump().items():
        setattr(db_message, key, value)
    try:
        db.commit()
        db.refresh(db_message)
        return db_message
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{message_id}", response_model=MessageModel)
def delete_message(message_id: str, db: SQLAlchemySession = Depends(get_db)):
    
    try:
        db_message = db.query(MessageSchema).filter(MessageSchema.message_id == message_id).first()
    except HTTPException as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db_message is None:
            raise HTTPException(status_code=404, detail="Message not found")

    try:   
        db.delete(db_message)
        db.commit()
        return db_message
    except HTTPException as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

# List all messages
@router.get("/", response_model=List[MessageModel])
def list_messages(skip: int = 0, limit: int = 10, db: SQLAlchemySession = Depends(get_db)):
    try:
        messages = db.query(MessageSchema).offset(skip).limit(limit).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if not messages:
            raise HTTPException(status_code=404, detail="Messages not found")
        return messages
    