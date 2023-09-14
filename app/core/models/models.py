import uu
from fastapi.utils import generate_unique_id
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
import uuid


def generate_session_id():
    return str(uuid.uuid4())

class SessionBase(BaseModel):
    created_at: datetime
    ended_at: Optional[datetime] = None
    user_email: Optional[EmailStr] = None
    user_name: Optional[str] = None
    user_role: Optional[str] = None
    data_user_consent: Optional[bool] = False

class SessionCreate(SessionBase):
    session_id: str = Field(default_factory=generate_session_id)

class Session(SessionBase):
    session_id: str 

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    created_at: datetime
    exchange: str
    message_type: str
    session_id: str

class MessageCreate(MessageBase):
    message_id: str = Field(default_factory=generate_session_id)

class Message(MessageBase):
    message_id: str 

    class Config:
        orm_mode = True
