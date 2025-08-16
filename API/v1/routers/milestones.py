from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from v1.auth import get_current_user
from v1.models import User, ProjectMember, Milestone
from v1.schemas import MilestoneCreate, MilestoneResponse
from .tasks import check_project_membership

router = APIRouter(
    tags=["milestones"],
)

@router.post("/projects/{project_id}/milestones/", response_model=MilestoneResponse, status_code=status.HTTP_201_CREATED)
def create_milestone_for_project(
    project_id: int,
    milestone: MilestoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    membership = check_project_membership(project_id, current_user.id, db)
    if membership.role.name != 'manager':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only project managers can create milestones")

    db_milestone = Milestone(**milestone.dict(), project_id=project_id)
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone

@router.get("/projects/{project_id}/milestones/", response_model=List[MilestoneResponse])
def read_milestones_for_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_project_membership(project_id, current_user.id, db)
    return db.query(Milestone).filter(Milestone.project_id == project_id).all()

@router.put("/milestones/{milestone_id}", response_model=MilestoneResponse)
def update_milestone(
    milestone_id: int,
    milestone_update: MilestoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if not db_milestone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Milestone not found")

    membership = check_project_membership(db_milestone.project_id, current_user.id, db)
    if membership.role.name != 'manager':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only project managers can update milestones")

    for key, value in milestone_update.dict().items():
        setattr(db_milestone, key, value)

    db.commit()
    db.refresh(db_milestone)
    return db_milestone

@router.delete("/milestones/{milestone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_milestone(
    milestone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if not db_milestone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Milestone not found")

    membership = check_project_membership(db_milestone.project_id, current_user.id, db)
    if membership.role.name != 'manager':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only project managers can delete milestones")

    db.delete(db_milestone)
    db.commit()
    return