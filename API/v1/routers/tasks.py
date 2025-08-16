from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from core.database import get_db
from pydantic import BaseModel
from v1.auth import get_current_user
from v1.models import User, ProjectMember, Task, Notification
from v1.schemas import TaskCreate, TaskResponse

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: str = 'pending'
    assignee_id: int | None = None
    due_date: date | None = None

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    project_id: int
    class Config:
        from_attributes = True

router = APIRouter(
    tags=["tasks"],
)

def check_project_membership(project_id: int, user_id: int, db: Session):
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()
    if not membership:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this project")
    return membership

@router.post("/projects/{project_id}/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_for_project(
    project_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_project_membership(project_id, current_user.id, db)
    
    if task.assignee_id:
        check_project_membership(project_id, task.assignee_id, db)

    db_task = Task(**task.dict(), project_id=project_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    if db_task.assignee_id:
        notification_msg = f"You have been assigned a new task: '{db_task.title}'"
        notification = Notification(user_id=db_task.assignee_id, message=notification_msg)
        db.add(notification)
        db.commit()

    return db_task

@router.get("/projects/{project_id}/tasks/", response_model=List[TaskResponse])
def read_tasks_for_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_project_membership(project_id, current_user.id, db)
    return db.query(Task).filter(Task.project_id == project_id).all()

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    check_project_membership(db_task.project_id, current_user.id, db)
    
    original_assignee_id = db_task.assignee_id
        
    update_data = task_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
        
    db.commit()
    db.refresh(db_task)
    
    new_assignee_id = db_task.assignee_id
    if new_assignee_id and new_assignee_id != original_assignee_id:
        notification_msg = f"You have been assigned a new task: '{db_task.title}'"
        notification = Notification(user_id=new_assignee_id, message=notification_msg)
        db.add(notification)
        db.commit()

    return db_task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
    membership = check_project_membership(db_task.project_id, current_user.id, db)

    if membership.role.name != 'manager':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only project managers can delete tasks")
        
    db.delete(db_task)
    db.commit()
    return