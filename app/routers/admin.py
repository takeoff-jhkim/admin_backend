from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from .. import crud, schemas
from ..utils.security import create_access_token, get_password_hash, get_current_user
from ..models import User
from app.database import get_db

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=list[schemas.UserOut])
def read_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
        if current_user.role == "admin":
            return crud.get_all_users(db)
        else:
            raise HTTPException(status_code=403, detail="Only Admin")

@router.patch("/users/{user_id}", response_model=schemas.UserOut)
def change_user_role(user_id: int, body: schemas.UpdateUserRole, db: Session = Depends(get_db)):
    return crud.update_user_role(db, user_id, body.role)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)

@router.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 중복 이메일 검사 (선택 사항)
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = models.User(
        email=user.email,
        name=user.name,
        role=user.role,
        nickname=user.nickname,
        password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"email": current_user}