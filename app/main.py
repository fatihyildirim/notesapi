import os
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from . import models, db, schemas, auth


app = FastAPI(title="Notes")
models.Base.metadata.create_all(bind=db.engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(db.get_db)):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.UserModel).filter(models.UserModel.username == username).first()
    return user

@app.get("/")
def root():
    return {
        "version": "0.1",
        "title": "Notes",
        "description": "A simple notes API"
    }

@app.post("/token")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(db.get_db)
    ):
    user = db.query(models.UserModel).filter(models.UserModel.username == form_data.username).first()

    if not user or auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = auth.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(
        user: schemas.UserCreate,
        db: Session = Depends(db.get_db)
    ):
    db_user = db.query(models.UserModel).filter(models.UserModel.username == user.username).first()

    if db_user:
        HTTPException(status_code=400, detail="User already exists")

    hashed_password = auth.get_password_hash(user.password)

    new_user = models.UserModel(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "id": new_user.id}

@app.get("/users", response_model=list[schemas.UserResponse])
def read_users(
        db: Session = Depends(db.get_db)
    ):
    users = db.query(models.UserModel).all()

    return users

@app.get("/notes", response_model=list[schemas.NoteResponse])
def read_notes(
        skip: int = 0, limit: int = 10,
        db: Session = Depends(db.get_db),
        current_user: models.UserModel = Depends(get_current_user),
    ):
    notes = db.query(models.NoteModel)\
        .filter(models.NoteModel.owner_id == current_user.id)\
        .order_by(models.NoteModel.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

    return notes

@app.get("/notes/search", response_model=list[schemas.NoteResponse])
def search_notes(
        query: Optional[str] = None,
        category: Optional[str] = None,
        db: Session = Depends(db.get_db),
        current_user: models.UserModel = Depends(get_current_user),
    ):
    search_query = db.query(models.NoteModel).filter(models.NoteModel.owner_id == current_user.id)

    if query:
        search_query = search_query.filter(
            models.NoteModel.title.ilike(f"%{query}%"),
            models.NoteModel.content.ilike(f"%{query}%"),
        )

    if category:
        search_query = search_query.filter(models.NoteModel.category == category)

    return search_query.all()

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
        current_user: models.UserModel = Depends(get_current_user)
    ):
    db_note = models.NoteModel(**note.model_dump(), owner_id=current_user.id)
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