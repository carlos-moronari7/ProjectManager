from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from core.database import get_db
from v1.auth import get_current_user
from v1.models import User, Role, Project, ProjectMember
from v1.schemas import ProjectCreate, ProjectResponse, MemberCreate, ProjectMemberResponse

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
    db.refresh(db_project)
    
    # Eagerly load the members for the response
    db.query(Project).filter(Project.id == db_project.id).options(
        joinedload(Project.project_members).joinedload(ProjectMember.user).joinedload(User.role),
        joinedload(Project.project_members).joinedload(ProjectMember.role)
    ).first()
    
    return db_project

@router.get("/", response_model=List[ProjectResponse])
def read_projects_for_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = db.query(Project).join(ProjectMember).filter(
        ProjectMember.user_id == current_user.id
    ).options(
        joinedload(Project.project_members).joinedload(ProjectMember.user).joinedload(User.role),
        joinedload(Project.project_members).joinedload(ProjectMember.role)
    ).distinct().all()
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # First check for membership
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Project not found or you do not have access")

    # Then fetch the project with all its data
    project = db.query(Project).filter(Project.id == project_id).options(
        joinedload(Project.project_members).joinedload(ProjectMember.user).joinedload(User.role),
        joinedload(Project.project_members).joinedload(ProjectMember.role)
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
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