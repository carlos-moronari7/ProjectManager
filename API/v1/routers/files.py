from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from minio import Minio
import uuid
from typing import List

from core.database import get_db
from core.minio_client import get_minio_client
from v1.auth import get_current_user
from v1.models import User, ProjectFile
from v1.schemas import ProjectFileResponse
from .tasks import check_project_membership
from core.config import settings

router = APIRouter(
    tags=["files"],
)

@router.post("/projects/{project_id}/files", response_model=ProjectFileResponse, status_code=status.HTTP_201_CREATED)
def upload_file_for_project(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    minio_client: Minio = Depends(get_minio_client)
):
    check_project_membership(project_id, current_user.id, db)

    file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
    object_name = f"{uuid.uuid4()}.{file_extension}"
    
    try:
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        minio_client.put_object(
            bucket_name=settings.MINIO_BUCKET_NAME,
            object_name=object_name,
            data=file.file,
            length=file_size,
            content_type=file.content_type
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to upload file to storage: {e}")

    db_file = ProjectFile(
        project_id=project_id,
        file_name=file.filename,
        object_name=object_name,
        content_type=file.content_type,
        file_size=file_size,
        uploaded_by_id=current_user.id
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file

@router.get("/projects/{project_id}/files", response_model=List[ProjectFileResponse])
def list_files_for_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_project_membership(project_id, current_user.id, db)
    return db.query(ProjectFile).filter(ProjectFile.project_id == project_id).all()

@router.get("/files/{file_id}/download")
def get_file_download_link(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    minio_client: Minio = Depends(get_minio_client)
):
    db_file = db.query(ProjectFile).filter(ProjectFile.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        
    check_project_membership(db_file.project_id, current_user.id, db)
    
    try:
        presigned_url = minio_client.presigned_get_object(
            bucket_name=settings.MINIO_BUCKET_NAME,
            object_name=db_file.object_name,
            expires=timedelta(hours=1)
        )
        return {"url": presigned_url}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not generate download link: {e}")

@router.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    minio_client: Minio = Depends(get_minio_client)
):
    db_file = db.query(ProjectFile).filter(ProjectFile.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    membership = check_project_membership(db_file.project_id, current_user.id, db)

    if membership.role.name != 'manager' and db_file.uploaded_by_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this file")

    try:
        minio_client.remove_object(settings.MINIO_BUCKET_NAME, db_file.object_name)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete file from storage: {e}")

    db.delete(db_file)
    db.commit()
    return