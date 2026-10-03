import sys
file_path = "D:/DemoCN2026/dblearning/backend/app/models/models.py"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "recommend" in content.lower():
            for line in content.split("\n"):
                if "recommend" in line.lower() or "class" in line:
                    print(line)
        else:
            print("No recommendation models found in models.py")
except Exception as e:
    print(e)
