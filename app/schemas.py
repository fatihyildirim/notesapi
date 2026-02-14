from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class NoteBase(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class NoteResponse(NoteBase):
    id: int
    class Config:
        from_attributes = True

class NoteCreate(NoteBase):
    title: str = Field(min_length=3, max_length=100, description="Note Title")
    content: str = Field(min_length=5, max_length=1000, description="Note Content")
    category: str = Field(default="Genel", max_length=20)
