import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Register.jsx"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(120, min(170, len(lines))):
            sys.stdout.buffer.write(f"{i+1}: {lines[i]}".encode("utf-8"))
except Exception as e:
    print(f"Error: {e}")
