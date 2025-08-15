from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from v1.auth import get_current_user
from v1.models import Role, User
from .users import UserResponse, RoleResponse
from v1.schemas import UserResponse, RoleResponse

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.role or current_user.role.name != 'superadmin':
        raise HTTPException(status_code=403, detail="This action requires admin privileges")
    return current_user

@router.get("/roles", response_model=List[RoleResponse])
def get_all_roles(db: Session = Depends(get_db), admin: User = Depends(get_current_admin_user)):
    return db.query(Role).all()

@router.put("/users/{user_id}/role/{role_id}", response_model=UserResponse)
def change_user_role(
    user_id: int, 
    role_id: int, 
    db: Session = Depends(get_db), 
    admin: User = Depends(get_current_admin_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
        
    user.role_id = role_id
    db.commit()
    db.refresh(user)
    return user