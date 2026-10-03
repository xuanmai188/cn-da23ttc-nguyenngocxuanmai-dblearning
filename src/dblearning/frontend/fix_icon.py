file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/Statistics.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("UserCheckIcon", "AcademicCapIcon")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Replaced UserCheckIcon with AcademicCapIcon")
