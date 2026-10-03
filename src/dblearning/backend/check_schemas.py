import os
files = ["D:/DemoCN2026/dblearning/backend/app/schemas/topic.py", "D:/DemoCN2026/dblearning/backend/app/schemas/content.py"]
for f in files:
    if os.path.exists(f):
        print(f"\n--- {f} ---")
        with open(f, "r", encoding="utf-8") as file:
            print(file.read())
