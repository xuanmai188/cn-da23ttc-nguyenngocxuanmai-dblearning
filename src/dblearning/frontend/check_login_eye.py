file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Login.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "Eye" in line:
        print(f"{i+1}: {line.strip()}")
