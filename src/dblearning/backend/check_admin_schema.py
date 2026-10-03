import sys
file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for j in range(550, 580):
    try:
        sys.stdout.buffer.write(f"{j}: {lines[j]}".encode("utf-8"))
    except:
        pass
