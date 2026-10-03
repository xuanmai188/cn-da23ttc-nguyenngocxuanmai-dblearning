import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/AdminDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
if "so với tháng trước" in content:
    print("Found 'so với tháng trước'")
else:
    print("NOT FOUND 'so với tháng trước'")
