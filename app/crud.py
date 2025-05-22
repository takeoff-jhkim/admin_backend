from sqlalchemy.orm import Session
from app.utils.security import verify_password
from app import models, schemas
from sqlalchemy import asc, desc, func
from typing import Optional


def get_all_users(db: Session, order: Optional[str] = None):
    query = db.query(models.User)

    if order:
        reverse = False
        order_key = order
        if order.startswith("-"):
            reverse = True
            order_key = order[1:]
        
        sort_column = getattr(models.User, order_key, None)
        if sort_column is not None:
            query = query.order_by(desc(sort_column) if reverse else asc(sort_column))

    return query.all()

def update_user_role(db: Session, user_id: int, role: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.role = role
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

def create_user(db: Session, user: schemas.UserCreate):
    new_user = models.User(
        email=user.email,
        name=user.name,
        role=user.role,
        nickname=user.nickname  # ✅ 여기서 저장!
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user
