import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/AdminDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "Tổng người dùng" in line or "stats.user_growth_rate" in line:
        start = max(0, i-5)
        for j in range(start, min(len(lines), start+20)):
            try:
                sys.stdout.buffer.write(f"{j+1}: {lines[j]}".encode("utf-8"))
            except:
                pass
        break
