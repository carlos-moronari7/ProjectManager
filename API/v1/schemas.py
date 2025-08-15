from pydantic import BaseModel, EmailStr
from datetime import date

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
    role: RoleResponse
    class Config:
        from_attributes = True

# --- Project Schemas ---
class ProjectBase(BaseModel):
    name: str
    description: str | None = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
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
        
# --- Task Schemas ---
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

# --- Comment Schemas ---
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    task_id: int
    author_id: int
    class Config:
        from_attributes = True

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None