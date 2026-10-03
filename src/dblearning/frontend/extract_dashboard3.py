file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/AdminDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("recentActivities")
with open("D:/DemoCN2026/dblearning/frontend/debug_dashboard.txt", "w", encoding="utf-8") as out:
    out.write(content[max(0, idx-1000):idx+1000])
