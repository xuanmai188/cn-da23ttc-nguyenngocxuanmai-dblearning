import os

directory = "D:/DemoCN2026/dblearning/frontend/src/pages/admin"
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".jsx"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                if "/admin/reports" in content or "Xem" in content:
                    print(f"Found in: {file}")
                    # print snippet
                    idx = content.find("/admin/reports")
                    if idx == -1:
                        idx = content.find("Xem ")
                    print(content[max(0, idx-100):idx+200])
