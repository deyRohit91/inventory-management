from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import UserCreate
from repository import user_repo
from core.auth import hash_password, verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["v1 - Auth"]        
)

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = user_repo.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="User exists")

    hashed = hash_password(user.password)
    user_repo.create_user(db, user.username, hashed)

    return {"message": "User created"}


@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_repo.get_user_by_username(db, user.username)

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username})

    return {"access_token": token, "token_type": "bearer"}