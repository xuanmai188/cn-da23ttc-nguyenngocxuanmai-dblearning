file_path = "D:/DemoCN2026/dblearning/backend/app/api/api.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

if "from app.api.endpoints import reports" not in content:
    content = content.replace("from app.api.endpoints import auth, admin, learning, quiz, recommendation, student_survey", "from app.api.endpoints import auth, admin, learning, quiz, recommendation, student_survey, reports")
    content = content + "\napi_router.include_router(reports.router, prefix=\"/admin/reports\", tags=[\"reports\"])\n"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Registered reports.py in api.py")
