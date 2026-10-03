file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        if "UserItem(" in line:
            print(line.strip())
