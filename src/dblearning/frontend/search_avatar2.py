import os
for root, dirs, files in os.walk("D:/DemoCN2026/dblearning/frontend/src"):
    for file in files:
        if file.endswith((".jsx", ".js")):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        if "charAt(0)" in line or "[0]" in line:
                            if "charAt(0)" in line and ("user" in line or "name" in line or "email" in line):
                                print(f"{path}:{i+1}: {line.strip()}")
            except Exception:
                pass
