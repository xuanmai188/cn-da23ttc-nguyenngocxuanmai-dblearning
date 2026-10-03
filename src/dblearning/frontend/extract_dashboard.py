file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/AdminDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("Xem ")
with open("D:/DemoCN2026/dblearning/frontend/debug.txt", "w", encoding="utf-8") as out:
    out.write(content[max(0, idx-300):idx+500])
