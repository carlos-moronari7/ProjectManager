from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from v1.auth import get_current_user
from v1.models import User, Task, TimeLog, ProjectMember
from v1.schemas import TimeLogCreate, TimeLogResponse

router = APIRouter(
    tags=["time-tracking"],
)

def get_task_and_check_membership(task_id: int, user_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == task.project_id,
        ProjectMember.user_id == user_id
    ).first()
    
    if not membership:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this task")
    
    return task

@router.post("/tasks/{task_id}/timelogs/", response_model=TimeLogResponse, status_code=status.HTTP_201_CREATED)
def create_time_log_for_task(
    task_id: int,
    time_log: TimeLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_task_and_check_membership(task_id, current_user.id, db)
    
    db_time_log = TimeLog(**time_log.dict(), task_id=task_id, user_id=current_user.id)
    db.add(db_time_log)
    db.commit()
    db.refresh(db_time_log)
    return db_time_log

@router.get("/tasks/{task_id}/timelogs/", response_model=List[TimeLogResponse])
def read_time_logs_for_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_task_and_check_membership(task_id, current_user.id, db)
    return db.query(TimeLog).filter(TimeLog.task_id == task_id).all()

@router.delete("/timelogs/{time_log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_time_log(
    time_log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_time_log = db.query(TimeLog).filter(TimeLog.id == time_log_id).first()
    
    if not db_time_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Time log not found")
        
    if db_time_log.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this time log")
        
    db.delete(db_time_log)
    db.commit()
    return