file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "def update_user" in line:
        start = i
        break

for j in range(start, start+15):
    try:
        import sys
        sys.stdout.buffer.write(f"{j}: {lines[j]}".encode("utf-8"))
    except:
        pass
