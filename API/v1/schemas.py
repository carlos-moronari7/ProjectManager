from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import List, Optional

# --- Role Schemas ---
class RoleResponse(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    availability_status: str
    role: RoleResponse
    class Config:
        from_attributes = True

# --- Project Member Schemas ---
class MemberCreate(BaseModel):
    user_id: int
    role_id: int

class ProjectMemberResponse(BaseModel):
    role: RoleResponse
    user: UserResponse
    class Config:
        from_attributes = True

class MilestoneBase(BaseModel):
    name: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: str = 'pending'

class MilestoneCreate(MilestoneBase):
    pass

class MilestoneResponse(MilestoneBase):
    id: int
    project_id: int
    created_at: datetime
    class Config:
        from_attributes = True
        
# --- Project Schemas ---
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    status: str = 'in_progress'

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    progress: int
    project_members: List[ProjectMemberResponse] = []
    class Config:
        from_attributes = True

# --- File Schemas ---
class ProjectFileResponse(BaseModel):
    id: int
    project_id: int
    file_name: str
    content_type: Optional[str] = None
    file_size: Optional[int] = None
    uploaded_at: datetime
    uploaded_by_id: int
    class Config:
        from_attributes = True

# --- Task Schemas ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = 'pending'
    priority: str = 'medium'
    assignee_id: Optional[int] = None
    due_date: Optional[date] = None
    reminder_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    project_id: int
    created_at: datetime
    files: List[ProjectFileResponse] = []
    class Config:
        from_attributes = True

class TaskDependencyCreate(BaseModel):
    depends_on_task_id: int

# --- Mention Schemas ---
class MentionResponse(BaseModel):
    user: UserResponse
    class Config:
        from_attributes = True

# --- Comment Schemas ---
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    mentioned_user_ids: Optional[List[int]] = None

class CommentResponse(CommentBase):
    id: int
    task_id: int
    author_id: int
    created_at: datetime
    mentions: List[MentionResponse] = []
    class Config:
        from_attributes = True

# --- Time Log Schemas ---
class TimeLogBase(BaseModel):
    start_time: datetime
    end_time: Optional[datetime] = None
    notes: Optional[str] = None

class TimeLogCreate(TimeLogBase):
    pass

class TimeLogResponse(TimeLogBase):
    id: int
    task_id: int
    user_id: int
    class Config:
        from_attributes = True

# --- Issue Schemas ---
class IssueBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = 'open'
    severity: str = 'medium'
    assignee_id: Optional[int] = None

class IssueCreate(IssueBase):
    pass

class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    severity: Optional[str] = None
    assignee_id: Optional[int] = None

class IssueResponse(IssueBase):
    id: int
    project_id: int
    reporter_id: int
    created_at: datetime
    resolved_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# --- Report Schemas ---
class TeamWorkloadResponse(BaseModel):
    assignee_id: int
    email: EmailStr
    open_tasks_count: int

class ProjectSummaryResponse(BaseModel):
    project_id: int
    project_name: str
    budget: Optional[float]
    total_tasks: int
    completed_tasks: int
    progress_percentage: float
    tasks_by_status: dict

# --- Notification Schemas ---
class NotificationResponse(BaseModel):
    id: int
    user_id: int
    message: str
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None