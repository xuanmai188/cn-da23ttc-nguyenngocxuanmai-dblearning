file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_schemas = """class UserDetailStats(BaseModel):
    completed_lessons: int
    taken_quizzes: int
    avg_score: float
    total_hours: float

class UserDetailResponse(UserItem):
    stats: UserDetailStats
    phone_number: Optional[str] = None

class UserHistoryItem(BaseModel):
    id: int
    action: str
    target: str
    target_type: str
    created_at: datetime
    time_ago: str

class UserHistoryResponse(BaseModel):
    history: List[UserHistoryItem]
"""

# Append at the end of the file
with open(file_path, "a", encoding="utf-8") as f:
    f.write("\n" + new_schemas)
print("Updated admin.py schemas for User Detail and History")
