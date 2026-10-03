import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserDetailPanel.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "Thông tin" in line and "Tiến độ học tập" in line:
        pass
    if "Tên đăng nhập" in line:
        start = i - 5
        for j in range(max(0, start), min(len(lines), start+45)):
            try:
                sys.stdout.buffer.write(f"{j}: {lines[j]}".encode("utf-8"))
            except:
                pass
        break
