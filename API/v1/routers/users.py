from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from v1.models import User, Role
from v1.schemas import UserCreate, UserResponse, Token
from core.database import get_db
from pydantic import BaseModel, EmailStr
from v1 import auth
from v1.models import User, Role

class RoleResponse(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    availability_status: str
    role: RoleResponse
    class Config:
        from_attributes = True

router = APIRouter()

@router.post("/users/", response_model=UserResponse, tags=["users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    member_role = db.query(Role).filter(Role.name == "member").first()
    if not member_role:
        raise HTTPException(status_code=500, detail="Default 'member' role not found.")

    hashed_password = auth.get_password_hash(user.password)
    db_user = User(
        email=user.email, 
        hashed_password=hashed_password,
        role_id=member_role.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/me/", response_model=UserResponse, tags=["users"])
def read_users_me(current_user: User = Depends(auth.get_current_user)):
    return current_user

@router.get("/users/", response_model=List[UserResponse], tags=["users"])
def read_users(db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    if current_user.role.name not in ['superadmin', 'manager']:
        raise HTTPException(status_code=403, detail="Not authorized to view users")
    return db.query(User).all()

@router.post("/token", response_model=auth.Token, tags=["authentication"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}