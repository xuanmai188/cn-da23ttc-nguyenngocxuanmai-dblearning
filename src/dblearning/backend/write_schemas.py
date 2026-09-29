file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/admin.py"
content = """from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class DashboardStats(BaseModel):
    total_users: int
    active_users: int
    total_sessions: int
    total_quizzes: int
    avg_completion_rate: float

class UserItem(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserList(BaseModel):
    users: List[UserItem]
    total: int
"""
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Schemas written")
