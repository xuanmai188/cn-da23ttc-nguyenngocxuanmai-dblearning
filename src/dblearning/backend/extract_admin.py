file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("def get_dashboard_stats")
with open("D:/DemoCN2026/dblearning/backend/debug_admin.txt", "w", encoding="utf-8") as out:
    out.write(content[max(0, idx+1000):idx+3000])
