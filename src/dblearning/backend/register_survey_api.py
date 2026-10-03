file_path = "D:/DemoCN2026/dblearning/backend/app/api/api.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

if "student_survey" not in content:
    content = content.replace(
        "from app.api.endpoints import auth, admin, learning, quiz, recommendation",
        "from app.api.endpoints import auth, admin, learning, quiz, recommendation, student_survey"
    )
    content += "\napi_router.include_router(student_survey.router, prefix=\"/survey\", tags=[\"survey\"])\n"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Registered student_survey in api.py")
else:
    print("Already registered.")
