from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    role = Column(String, default="user")  # ← ENUM → STRING 변경
    created_at = Column(DateTime, default=datetime.utcnow)

    nickname = Column(String, nullable=True)
    # models.py
    password = Column(String, nullable=False)

