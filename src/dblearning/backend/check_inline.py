file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

import sys
for i, line in enumerate(lines):
    if "class UserCreate(BaseModel):" in line:
        start = i
        break

for j in range(start - 2, start + 18):
    try:
        sys.stdout.buffer.write(f"{j}: {lines[j]}".encode("utf-8"))
    except Exception:
        pass
