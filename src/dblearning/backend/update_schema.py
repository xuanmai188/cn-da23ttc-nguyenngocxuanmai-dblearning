file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/user.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add phone_number to UserBase
if "phone_number: Optional[str] = None" not in content:
    content = content.replace(
        "avatar_url: Optional[str] = None",
        "avatar_url: Optional[str] = None\n    phone_number: Optional[str] = None"
    )

# Add phone_number to UserUpdate
if "phone_number: Optional[str] = None" not in content.split("UserUpdate(BaseModel):")[1]:
    content = content.replace(
        "class UserUpdate(BaseModel):",
        "class UserUpdate(BaseModel):\n    phone_number: Optional[str] = None"
    )

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("schemas/user.py updated")
