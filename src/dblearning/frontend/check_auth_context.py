import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/context/AuthContext.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        if "register" in line:
            print(line.strip())
