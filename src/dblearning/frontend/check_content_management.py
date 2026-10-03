import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/ContentManagement.jsx"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if "Tài liệu" in line or "documents" in line:
                start = max(0, i-2)
                for j in range(start, min(len(lines), start+10)):
                    try:
                        sys.stdout.buffer.write(f"{j+1}: {lines[j]}".encode("utf-8"))
                    except:
                        pass
                break
except Exception as e:
    print(e)
