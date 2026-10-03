import os

def search_files(directory, search_str):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith((".jsx", ".js")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            if search_str in line or "charAt(0)" in line or "[0]" in line:
                                if search_str in line or "full_name" in line or "email" in line or "user." in line:
                                    print(f"{path}:{i+1}: {line.strip()}")
                except Exception:
                    pass

search_files("D:/DemoCN2026/dblearning/frontend/src", "")
