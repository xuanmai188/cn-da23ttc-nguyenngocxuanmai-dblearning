file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/learning.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "avg_quiz_score: float\n    last_updated: datetime",
    "avg_quiz_score: float\n    learning_streak: int = 1\n    last_updated: datetime"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("schemas/learning.py updated")
