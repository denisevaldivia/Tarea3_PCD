from sqlalchemy import Column, Integer, String, JSON
from database import Base

# Schema de la base de datos
class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    user_email = Column(String, nullable=False, unique=True)
    age = Column(Integer, nullable=True)
    zip = Column(String, nullable=True)
    recommendations = Column(JSON, nullable=False)
