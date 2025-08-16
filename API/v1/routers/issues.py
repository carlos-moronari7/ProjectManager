from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from v1.auth import get_current_user
from v1.models import User, Issue
from v1.schemas import IssueCreate, IssueUpdate, IssueResponse
from .tasks import check_project_membership

router = APIRouter(
    tags=["issues"],
)

@router.post("/projects/{project_id}/issues/", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
def create_issue_for_project(
    project_id: int,
    issue: IssueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_project_membership(project_id, current_user.id, db)
    
    db_issue = Issue(**issue.dict(), project_id=project_id, reporter_id=current_user.id)
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue

@router.get("/projects/{project_id}/issues/", response_model=List[IssueResponse])
def read_issues_for_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_project_membership(project_id, current_user.id, db)
    return db.query(Issue).filter(Issue.project_id == project_id).all()

@router.put("/issues/{issue_id}", response_model=IssueResponse)
def update_issue(
    issue_id: int,
    issue_update: IssueUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not db_issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
    
    check_project_membership(db_issue.project_id, current_user.id, db)
        
    update_data = issue_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_issue, key, value)
        
    db.commit()
    db.refresh(db_issue)
    return db_issue