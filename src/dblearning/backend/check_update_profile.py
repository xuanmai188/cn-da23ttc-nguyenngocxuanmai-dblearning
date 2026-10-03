import sys
file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/auth.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "def update_profile(" in line:
        start = i
        break
for j in range(start, min(len(lines), start+20)):
    try:
        sys.stdout.buffer.write(f"{j}: {lines[j]}".encode("utf-8"))
    except:
        pass
