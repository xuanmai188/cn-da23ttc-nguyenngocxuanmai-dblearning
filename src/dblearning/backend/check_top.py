file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
import sys
for i in range(5, 15):
    try:
        sys.stdout.buffer.write(f"{i}: {lines[i]}".encode("utf-8"))
    except:
        pass
