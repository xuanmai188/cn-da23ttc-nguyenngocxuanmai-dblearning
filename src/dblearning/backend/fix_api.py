file_path = "D:/DemoCN2026/dblearning/backend/app/api/api.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("from app.api.endpoints import auth, learning, quiz, recommendation, admin, student_survey", "from app.api.endpoints import auth, learning, quiz, recommendation, admin, student_survey, reports")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed reports import in api.py")
