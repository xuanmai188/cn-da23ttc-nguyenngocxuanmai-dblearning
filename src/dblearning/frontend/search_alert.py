import os
for root, dirs, files in os.walk("D:/DemoCN2026/dblearning/frontend/src"):
    for file in files:
        if file.endswith((".jsx", ".js")):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        if "Menu thao tác" in line:
                            print(f"{path}:{i+1}: {line.strip()}")
            except Exception:
                pass
