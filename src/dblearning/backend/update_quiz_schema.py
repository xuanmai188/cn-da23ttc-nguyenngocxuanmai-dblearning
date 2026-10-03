file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/quiz.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

schemas = """class QuizCreate(QuizBase):
    item_id: int

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    time_limit_minutes: Optional[int] = None
    pass_score: Optional[int] = None

class Quiz(QuizBase):"""

content = content.replace("class Quiz(QuizBase):", schemas)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated quiz.py schemas")
