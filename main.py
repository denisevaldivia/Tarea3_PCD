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
    user_id: int = Field(gt=-1)
    user_name: str = Field(min_length=1, max_length=100)
    user_email: EmailStr
    age: Optional[int] = Field(None, gt=-1, lt=101)
    zip: Optional[str] = Field(None, min_length=1, max_length=5)
    recommendations: List[str]

# ----- Endpoints -----
