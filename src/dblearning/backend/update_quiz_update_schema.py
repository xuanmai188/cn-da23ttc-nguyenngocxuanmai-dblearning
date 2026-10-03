file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/quiz.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

old_update = """class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    time_limit_minutes: Optional[int] = None
    pass_score: Optional[int] = None"""

new_update = """class QuizUpdate(BaseModel):
    item_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    time_limit_minutes: Optional[int] = None
    pass_score: Optional[int] = None"""

content = content.replace(old_update, new_update)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated QuizUpdate in schemas")
