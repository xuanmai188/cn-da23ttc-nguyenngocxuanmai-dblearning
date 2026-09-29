file_path = "D:/DemoCN2026/dblearning/backend/app/models/models.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "avg_quiz_score = Column(Float, default=0.0)",
    "avg_quiz_score = Column(Float, default=0.0)\n    learning_streak = Column(Integer, default=1)"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("models.py updated")
