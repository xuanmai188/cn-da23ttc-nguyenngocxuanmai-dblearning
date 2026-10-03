file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
if "contact_email: Optional[str] = None" not in content and "class UserItem(BaseModel):" in content:
    content = content.replace(
        "class UserItem(BaseModel):\n    id: int\n    email: str\n    full_name: str\n    role: str\n    is_active: bool\n    created_at: datetime\n    last_activity_at: Optional[str] = None",
        "class UserItem(BaseModel):\n    id: int\n    email: str\n    full_name: str\n    phone_number: Optional[str] = None\n    contact_email: Optional[str] = None\n    role: str\n    is_active: bool\n    created_at: datetime\n    last_activity_at: Optional[str] = None"
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Added phone_number and contact_email to UserItem schema")
else:
    print("Already added or schema format doesn't match")
