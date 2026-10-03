import sys
file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(15, 60):
    try:
        sys.stdout.buffer.write(f"{i+1}: {lines[i]}".encode("utf-8"))
    except:
        pass
