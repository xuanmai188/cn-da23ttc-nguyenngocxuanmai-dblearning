import os
for root, dirs, files in os.walk("D:/DemoCN2026/dblearning/frontend/src"):
    for file in files:
        if file.endswith(".jsx"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "Tm kim theo tn, tn ng nhp" in content or "tên đăng nhập" in content:
                        print(path)
            except:
                pass
