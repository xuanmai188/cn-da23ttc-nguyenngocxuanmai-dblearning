import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/content/QuizManagement.jsx"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(0, 20):
            sys.stdout.buffer.write(f"{i+1}: {lines[i]}".encode("utf-8"))
except Exception as e:
    print(e)
