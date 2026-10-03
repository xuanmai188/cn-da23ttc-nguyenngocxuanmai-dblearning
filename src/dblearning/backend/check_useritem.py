file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "class UserItem" in line:
        start = i
        break
for j in range(start, start+15):
    try:
        print(lines[j], end="")
    except Exception:
        pass
