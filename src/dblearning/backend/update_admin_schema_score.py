file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("avg_completion_rate: float", "avg_quiz_score: float")
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("schemas/admin.py updated")
