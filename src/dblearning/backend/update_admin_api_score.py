file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "sessions = db.query(LearningSession.completion_rate).all()\n    avg_rate = sum(s[0] for s in sessions) / len(sessions) if sessions else 0.0",
    "avg_score = db.query(func.avg(QuizResult.score)).scalar() or 0.0"
)

content = content.replace(
    '"avg_completion_rate": round(avg_rate * 100, 2)',
    '"avg_quiz_score": round(avg_score, 1)'
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("admin.py updated")
