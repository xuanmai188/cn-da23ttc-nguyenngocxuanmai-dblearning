import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "getItems" in line or "createItem" in line or "updateItem" in line:
        start = max(0, i-2)
        for j in range(start, min(len(lines), start+15)):
            try:
                sys.stdout.buffer.write(f"{j+1}: {lines[j]}".encode("utf-8"))
            except:
                pass
        break
