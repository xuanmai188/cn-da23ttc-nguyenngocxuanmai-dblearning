import os

file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add UserStats schema
user_stats_schema = """class UserStats(BaseModel):
    total: int
    students: int
    admins: int
    blocked: int
    growth_rate: float
    student_rate: float
    admin_rate: float
    blocked_rate: float

class UserItem"""
content = content.replace("class UserItem", user_stats_schema)

# Update UserItem to include last_activity_at
user_item_old = """class UserItem(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True"""
user_item_new = """class UserItem(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    last_activity_at: Optional[str] = None
    
    class Config:
        from_attributes = True"""
content = content.replace(user_item_old, user_item_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated admin schemas")
