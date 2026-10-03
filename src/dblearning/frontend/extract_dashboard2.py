file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/AdminDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("Hoạt động gần đây")
if idx == -1:
    # Try different encodings or just "Ho"
    idx = content.find("gần đây")
    
if idx != -1:
    with open("D:/DemoCN2026/dblearning/frontend/debug2.txt", "w", encoding="utf-8") as out:
        out.write(content[max(0, idx-100):idx+500])
