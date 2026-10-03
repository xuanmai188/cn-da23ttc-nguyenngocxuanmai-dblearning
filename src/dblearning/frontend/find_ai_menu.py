import sys
sys.stdout.reconfigure(encoding="utf-8")
file_path = "D:/DemoCN2026/dblearning/frontend/src/components/AdminLayout.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "Quản lý gợi ý AI" in line:
        start = max(0, i - 10)
        end = min(len(lines), i + 10)
        for j in range(start, end):
            print(f"{j+1}: {lines[j]}", end="")
        print("---")
        break
