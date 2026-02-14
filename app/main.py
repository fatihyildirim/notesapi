import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, db, schemas


app = FastAPI(title="Notes")
models.Base.metadata.create_all(bind=db.engine)

@app.get("/")
def root():
    return {
        "version": "0.1",
        "title": "Notes",
        "description": "A simple notes API"
    }

@app.get("/notes", response_model=list[schemas.NoteResponse])
def read_notes(
        db: Session = Depends(db.get_db)
    ):
    notes = db.query(models.NoteModel)\
        .order_by(models.NoteModel.created_at.desc())\
        .all()

    return notes

@app.get("/notes/{id}")
def get_note(
        id: int,
        db: Session = Depends(db.get_db)
    ):
    note = db.query(models.NoteModel).filter(models.NoteModel.id == id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note

@app.post("/notes", response_model=schemas.NoteResponse)
def create_note(
        note: schemas.NoteCreate,
        db: Session = Depends(db.get_db),
    ):
    db_note = models.NoteModel(**note.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note

@app.delete("/notes/{id}")
def delete_note(
        id: int,
        db: Session = Depends(db.get_db)
    ):
    note = db.query(models.NoteModel).filter(models.NoteModel.id == id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()

    return {"message": "Note deleted successfully"}