import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/content/QuizManagement.jsx"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        matches = [i for i, line in enumerate(lines) if "Thuộc Bài học" in line]
        if len(matches) > 1:
            start = max(0, matches[1]-2)
            for j in range(start, min(len(lines), start+15)):
                try:
                    sys.stdout.buffer.write(f"{j+1}: {lines[j]}".encode("utf-8"))
                except:
                    pass
except Exception as e:
    print(e)
