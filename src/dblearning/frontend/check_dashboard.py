import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/AdminDashboard.jsx"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "chart" in content.lower():
            print("AdminDashboard contains charts.")
        else:
            print("AdminDashboard has no charts.")
except Exception as e:
    print(e)
