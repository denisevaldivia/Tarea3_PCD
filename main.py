import os
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from dotenv import load_dotenv

import models
from database import engine, SessionLocal

# ----- Cargar variables de entorno (.env) -----
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ----- Iniciar app -----
app = FastAPI(title="Users API", version="1.0.0")

# ----- Crear tablas -----
models.Base.metadata.create_all(bind=engine)

# ----- Dependencia DB -----
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# ----- Seguridad por header -----
api_key_header = APIKeyHeader(name="X-API-Key", description="API key por header", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if API_KEY and api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials")

# ----- Esquema Pydantic -----
class User(BaseModel):
    user_name: str = Field(min_length=1, max_length=100)
    user_email: EmailStr
    age: Optional[int] = Field(None, gt=-1, lt=101)
    zip: Optional[str] = Field(None, min_length=1, max_length=5, alias='ZIP')
    recommendations: List[str]

# ----- Endpoints -----
@app.get("/")
def root():
    return {"message": "Users API up. See /docs"}

@app.post("/api/v1/users/", tags=["users"])
def create_user(user: User, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    # Checar si el email ya existe en la base
    usuarios_en_db = db.query(models.Users).filter(models.Users.user_email == user.user_email).first()
    if usuarios_en_db:
        raise HTTPException(status_code=409, detail=f"Email {user.user_email} : Already exists")

    # Si no esta, entonces se procede a añadirlo
    user_model = models.Users(
        user_name=user.user_name,
        user_email=user.user_email,
        age=user.age,
        zip=user.zip,
        recommendations=user.recommendations
    )

    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

@app.put("/api/v1/users/{user_id}", tags=["users"])
def update_user(user_id: int, user: User, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} : Does not exist")

    user_model.user_name = user.user_name
    user_model.user_email = user.user_email
    user_model.age = user.age
    user_model.zip = user.zip
    user_model.recommendations = user.recommendations

    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

@app.get("/api/v1/users/{user_id}", tags=["users"])
def get_user(user_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    list_user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if list_user is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} : Does not exist")
    return list_user

@app.delete("/api/v1/users/{user_id}", tags=["users"])
def delete_user(user_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} : Does not exist")

    db.delete(user_model)
    db.commit()
    return {"deleted_id": user_id}