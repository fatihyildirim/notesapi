from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
import datetime


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    notes = relationship("NoteModel", back_populates="owner")

class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("UserModel", back_populates="notes")
    category = Column(String)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)