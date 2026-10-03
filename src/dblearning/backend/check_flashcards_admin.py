import sys
file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        has_flashcard = False
        for i, line in enumerate(lines):
            if "/flashcards" in line:
                has_flashcard = True
                start = max(0, i-2)
                for j in range(start, min(len(lines), start+10)):
                    try:
                        sys.stdout.buffer.write(f"{j+1}: {lines[j]}".encode("utf-8"))
                    except:
                        pass
                print("---")
                break
        if not has_flashcard:
            print("No /flashcards endpoints found in admin.py")
except Exception as e:
    print(e)
