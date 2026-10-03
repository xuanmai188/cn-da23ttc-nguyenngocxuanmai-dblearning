import sys
file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/quiz.py"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if "class Flashcard" in line:
                start = max(0, i-2)
                for j in range(start, min(len(lines), start+20)):
                    try:
                        sys.stdout.buffer.write(f"{j+1}: {lines[j]}".encode("utf-8"))
                    except:
                        pass
                break
except Exception as e:
    print(e)
