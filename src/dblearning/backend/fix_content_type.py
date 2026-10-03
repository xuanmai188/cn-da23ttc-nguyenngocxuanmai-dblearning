file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/reports.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(".item_type", ".content_type")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed item_type to content_type in reports.py")
