from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from v1.auth import get_current_user
from v1.models import User, Task
from v1.schemas import TaskDependencyCreate, TaskResponse
from .tasks import check_project_membership

router = APIRouter(
    prefix="/tasks/{task_id}/dependencies",
    tags=["dependencies"],
)

def get_task_and_check_auth(task_id: int, user_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    check_project_membership(task.project_id, user_id, db)
    return task

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_task_dependency(
    task_id: int,
    dependency: TaskDependencyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_and_check_auth(task_id, current_user.id, db)
    depends_on_task = get_task_and_check_auth(dependency.depends_on_task_id, current_user.id, db)

    if task.project_id != depends_on_task.project_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tasks must be in the same project")

    if depends_on_task in task.dependencies:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dependency already exists")

    task.dependencies.append(depends_on_task)
    db.commit()
    return {"message": "Dependency added successfully"}

@router.get("/", response_model=List[TaskResponse])
def get_task_dependencies(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_and_check_auth(task_id, current_user.id, db)
    return task.dependencies

@router.delete("/{depends_on_task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task_dependency(
    task_id: int,
    depends_on_task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_and_check_auth(task_id, current_user.id, db)
    depends_on_task = get_task_and_check_auth(depends_on_task_id, current_user.id, db)
    
    if depends_on_task not in task.dependencies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dependency not found")
        
    task.dependencies.remove(depends_on_task)
    db.commit()
    return