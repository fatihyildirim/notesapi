from sqlalchemy import Column, Integer, String, DateTime, JSON
from .db import Base
import datetime


class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    category = Column(String)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)