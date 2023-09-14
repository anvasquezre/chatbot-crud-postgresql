from sqlalchemy import Column, Integer, String, ForeignKey, Table, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import uuid


Base = declarative_base()

class Session(Base):
    __tablename__ = 'sessions'
    session_id = Column(String(36), primary_key=True , nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    ended_at = Column(TIMESTAMP(timezone=True))
    user_email = Column(String)
    user_name = Column(String)
    user_role = Column(String)
    data_user_consent = Column(Boolean, nullable=False)

class Message(Base):
    __tablename__ = 'messages'
    message_id = Column(String(36), primary_key=True ,nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    exchange = Column(String, nullable=False)
    message_type = Column(String(1), nullable=False)
    session_id = Column(String(36), ForeignKey('sessions.session_id'))
    session = relationship('Session')