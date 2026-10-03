import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Register.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "type={showPassword ? \"text\" : \"password\"}" in line or "htmlFor=\"password\"" in line:
        start = max(0, i-5)
        for j in range(start, min(len(lines), start+40)):
            try:
                sys.stdout.buffer.write(f"{j+1}: {lines[j]}".encode("utf-8"))
            except:
                pass
        break
