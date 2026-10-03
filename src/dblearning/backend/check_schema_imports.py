file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "from app.schemas.learning import" in line or "from app.schemas.quiz import" in line:
        print(f"{i}: {line.strip()}")
