import os

for root, dirs, files in os.walk("D:/DemoCN2026/dblearning/backend"):
    if "venv" in root or "__pycache__" in root:
        continue
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f):
                        if "class UserUpdate" in line:
                            print(f"{path}:{i}: {line.strip()}")
            except:
                pass
