file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/learning.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

schemas = """class LearningItemCreate(LearningItemBase):
    pass

class LearningItemUpdate(BaseModel):
    topic_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    content_type: Optional[str] = None
    difficulty: Optional[str] = None
    content_url: Optional[str] = None
    content_body: Optional[str] = None
    keywords: Optional[List[str]] = None
    estimated_minutes: Optional[int] = None
    is_active: Optional[bool] = None

class LearningItem(LearningItemBase):"""

content = content.replace("class LearningItem(LearningItemBase):", schemas)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated learning.py")
