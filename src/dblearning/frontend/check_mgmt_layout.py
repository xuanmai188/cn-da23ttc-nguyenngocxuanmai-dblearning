import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/UserManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "return (" in line:
        start = i
        break
for j in range(start, min(len(lines), start+60)):
    try:
        sys.stdout.buffer.write(f"{j}: {lines[j]}".encode("utf-8"))
    except:
        pass
