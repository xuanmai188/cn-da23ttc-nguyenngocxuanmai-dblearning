file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_update_user = False
for i, line in enumerate(lines):
    if "def update_user" in line:
        in_update_user = True
    if in_update_user:
        print(f"{i}: {line}", end="")
        if "return user" in line:
            break
