file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/quiz.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Add QuestionCreate and QuestionUpdate
old_q = """class QuestionBase(BaseModel):
    content: str
    options: List[str]
    correct_option: int
    explanation: Optional[str] = None
    difficulty: str = "medium"
    order_index: int = 0"""

new_q = """class QuestionBase(BaseModel):
    content: str
    options: List[str]
    correct_option: int
    explanation: Optional[str] = None
    difficulty: str = "medium"
    order_index: int = 0

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    content: Optional[str] = None
    options: Optional[List[str]] = None
    correct_option: Optional[int] = None
    explanation: Optional[str] = None
    difficulty: Optional[str] = None
    order_index: Optional[int] = None"""

content = content.replace(old_q, new_q)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated quiz.py schemas")
