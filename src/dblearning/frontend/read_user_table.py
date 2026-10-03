import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserTable.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(50, min(len(lines), 150)):
    try:
        sys.stdout.buffer.write(f"{i+1}: {lines[i]}".encode("utf-8"))
    except:
        pass
