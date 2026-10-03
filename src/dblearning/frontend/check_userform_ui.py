import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFormModal.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "type=\"password\"" in line or "type={showPassword" in line:
        start = max(0, i-10)
        for j in range(start, min(len(lines), start+30)):
            try:
                sys.stdout.buffer.write(f"{j+1}: {lines[j]}".encode("utf-8"))
            except:
                pass
        break
