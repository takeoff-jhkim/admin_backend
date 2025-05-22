from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import models, crud, schemas
from app.utils.security import create_access_token, get_password_hash, get_current_user
from app.database import get_db
from typing import Optional

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=schemas.UserListResponse)
def read_users(
    page: int = Query(1, ge=1),
    size: int = Query(20,ge=1,le=100),
    order: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    all_users = crud.get_all_users(db, order=order)
    
    total_items = len(all_users)
    total_pages = (total_items + size - 1) // size
    has_next = page < total_pages

    start = (page - 1) * size
    end = start + size
    paginated_users = all_users[start:end]
        
    return schemas.UserListResponse(
        paging=schemas.PagingInfo(
        page=page,
        size=size,
        totalItems=total_items,
        totalPages=total_pages,
        hasNext=has_next,
    ),
    users=[schemas.UserOut.model_validate(user) for user in paginated_users]
)

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