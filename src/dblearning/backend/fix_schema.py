import os

file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/quiz.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_str = """class QuestionPublic(BaseModel):
    id: int
    content: str
    options: List[str]
    difficulty: str
    order_index: int"""

new_str = """class QuestionPublic(BaseModel):
    id: int
    content: str
    options: List[str]
    difficulty: str
    order_index: int

    class Config:
        from_attributes = True"""

content = content.replace(old_str, new_str)
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("QuestionPublic schema properly fixed!")
