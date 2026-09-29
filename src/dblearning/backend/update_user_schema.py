file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/user.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("email: EmailStr", "email: str")
content = content.replace("from pydantic import BaseModel, EmailStr, field_validator", "from pydantic import BaseModel, field_validator")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated user.py schema")
