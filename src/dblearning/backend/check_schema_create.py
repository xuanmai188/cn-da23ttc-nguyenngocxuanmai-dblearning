file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/user.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "class UserCreate" in line:
        start = i
        break
for j in range(start, start+10):
    print(lines[j], end="")
