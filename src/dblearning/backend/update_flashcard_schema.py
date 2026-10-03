file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/quiz.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

old_flashcard = """class FlashcardBase(BaseModel):
    question: str
    answer: str
    hint: Optional[str] = None
    order_index: int = 0"""

new_flashcard = """class FlashcardBase(BaseModel):
    question: str
    answer: str
    hint: Optional[str] = None
    order_index: int = 0

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    hint: Optional[str] = None
    order_index: Optional[int] = None"""

content = content.replace(old_flashcard, new_flashcard)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated quiz.py schemas with FlashcardCreate and FlashcardUpdate")
