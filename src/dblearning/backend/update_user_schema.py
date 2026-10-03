file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/user.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("role: Optional[str] = None", "role: Optional[str] = None\n    is_active: Optional[bool] = None")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Added is_active to UserUpdate schema")
