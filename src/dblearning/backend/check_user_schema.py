import sys
file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/user.py"
with open(file_path, "r", encoding="utf-8") as f:
    sys.stdout.buffer.write(f.read().encode("utf-8"))
