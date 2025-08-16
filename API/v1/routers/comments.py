from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from core.database import get_db
from v1.auth import get_current_user
from v1.models import User, Task, ProjectMember, Comment, Notification, Mention
from v1.schemas import CommentCreate, CommentResponse

router = APIRouter(
    tags=["comments"],
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

@router.post("/tasks/{task_id}/comments/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment_on_task(
    task_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_and_check_membership(task_id, current_user.id, db)
    
    db_comment = Comment(content=comment.content, task_id=task_id, author_id=current_user.id)
    db.add(db_comment)
    db.commit()

    # Handle mentions
    if comment.mentioned_user_ids:
        for user_id in set(comment.mentioned_user_ids):
            # Ensure mentioned user is part of the project
            check_project_membership(task.project_id, user_id, db)
            if user_id != current_user.id:
                mention = Mention(comment_id=db_comment.id, user_id=user_id)
                db.add(mention)
                
                notification_msg = f"@{current_user.email} mentioned you in a comment on task '{task.title}'"
                notification = Notification(user_id=user_id, message=notification_msg)
                db.add(notification)
        db.commit()
    
    db.refresh(db_comment)
    return db_comment

@router.get("/tasks/{task_id}/comments/", response_model=List[CommentResponse])
def read_comments_for_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_task_and_check_membership(task_id, current_user.id, db)
    return db.query(Comment).options(joinedload(Comment.mentions).joinedload(Mention.user)).filter(Comment.task_id == task_id).all()

@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        
    if db_comment.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this comment")
        
    db.delete(db_comment)
    db.commit()
    return