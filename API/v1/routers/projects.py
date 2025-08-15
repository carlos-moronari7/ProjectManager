from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from v1.models import User, Role, Project, ProjectMember
from v1.schemas import ProjectCreate, ProjectResponse, MemberCreate, ProjectMemberResponse

from core.database import get_db
from pydantic import BaseModel
from v1.auth import get_current_user
from v1.models import User, Role, Project, ProjectMember
from .users import UserResponse, RoleResponse

class ProjectBase(BaseModel):
    name: str
    description: str | None = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True

class MemberCreate(BaseModel):
    user_id: int
    role_id: int

class ProjectMemberResponse(BaseModel):
    role: RoleResponse
    user: UserResponse
    class Config:
        from_attributes = True

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role.name not in ["superadmin", "manager"]:
        raise HTTPException(status_code=403, detail="Not authorized to create projects")
        
    db_project = Project(**project.dict(), owner_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    manager_role = db.query(Role).filter(Role.name == "manager").first()
    if not manager_role:
        raise HTTPException(status_code=500, detail="'manager' role not found in database")

    first_member = ProjectMember(project_id=db_project.id, user_id=current_user.id, role_id=manager_role.id)
    db.add(first_member)
    db.commit()
    
    return db_project

@router.get("/", response_model=List[ProjectResponse])
def read_projects_for_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = db.query(Project).join(ProjectMember).filter(ProjectMember.user_id == current_user.id).all()
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).join(ProjectMember).filter(
        Project.id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or you do not have access")
    return project

@router.get("/{project_id}/members", response_model=List[ProjectMemberResponse])
def get_project_members(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    is_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    if not is_member:
        raise HTTPException(status_code=403, detail="You are not a member of this project")
    
    members = db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()
    return members

@router.post("/{project_id}/members", status_code=201)
def add_project_member(
    project_id: int, 
    member: MemberCreate,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    
    if not membership or membership.role.name != 'manager':
        raise HTTPException(status_code=403, detail="Not authorized to add members to this project")

    new_member_exists = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == member.user_id
    ).first()
    if new_member_exists:
        raise HTTPException(status_code=400, detail="User is already a member of this project")
        
    db_member = ProjectMember(project_id=project_id, user_id=member.user_id, role_id=member.role_id)
    db.add(db_member)
    db.commit()
    return {"message": "Member added successfully"}