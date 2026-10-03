import sys
file_path = "D:/DemoCN2026/dblearning/backend/app/models/models.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "class LearningItem" in line or "class Quiz" in line or "class FlashcardSet" in line:
        start = i
        for j in range(start, min(len(lines), start+15)):
            try:
                sys.stdout.buffer.write(f"{j+1}: {lines[j]}".encode("utf-8"))
            except:
                pass
        print("---")
