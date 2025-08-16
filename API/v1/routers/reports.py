from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from core.database import get_db
from v1.auth import get_current_user
from v1.models import User, Project, Task, ProjectMember
from v1.schemas import ProjectSummaryResponse

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)

@router.get("/projects/{project_id}/summary", response_model=ProjectSummaryResponse)
def get_project_summary(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this project")

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    tasks_by_status = db.query(Task.status, func.count(Task.id)).filter(
        Task.project_id == project_id
    ).group_by(Task.status).all()

    total_tasks = db.query(Task).filter(Task.project_id == project_id).count()
    completed_tasks = db.query(Task).filter(
        Task.project_id == project_id,
        Task.status == 'completed'
    ).count()
    
    progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    return {
        "project_id": project.id,
        "project_name": project.name,
        "budget": project.budget,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "progress_percentage": progress,
        "tasks_by_status": dict(tasks_by_status)
    }