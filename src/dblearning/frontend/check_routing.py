import sys
files = ["D:/DemoCN2026/dblearning/frontend/src/App.jsx", 
         "D:/DemoCN2026/dblearning/frontend/src/components/AdminLayout.jsx",
         "D:/DemoCN2026/dblearning/frontend/src/pages/admin/ContentManagement.jsx"]

for f in files:
    try:
        with open(f, "r", encoding="utf-8") as file:
            sys.stdout.buffer.write(f"\n--- {f} ---\n".encode("utf-8"))
            lines = file.readlines()
            for i, line in enumerate(lines):
                if "ContentManagement" in line or "admin/content" in line or "Chủ đề" in line or "Bài học" in line or "Quiz" in line:
                    start = max(0, i-5)
                    for j in range(start, min(len(lines), start+15)):
                        sys.stdout.buffer.write(f"{j}: {lines[j]}".encode("utf-8"))
                    break
    except Exception as e:
        sys.stdout.buffer.write(f"Error reading {f}: {e}\n".encode("utf-8"))
