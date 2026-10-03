import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserStatsCards.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "1000%" in line or "1000" in line:
        start = max(0, i-5)
        for j in range(start, min(len(lines), start+20)):
            try:
                sys.stdout.buffer.write(f"{j+1}: {lines[j]}".encode("utf-8"))
            except:
                pass
        break
