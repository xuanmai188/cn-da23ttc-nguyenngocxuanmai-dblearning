file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/UserManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "<UserDetailPanel" in line:
        start = i - 5
        for j in range(max(0, start), min(len(lines), start+10)):
            try:
                import sys
                sys.stdout.buffer.write(f"{j}: {lines[j]}".encode("utf-8"))
            except:
                pass
        break
