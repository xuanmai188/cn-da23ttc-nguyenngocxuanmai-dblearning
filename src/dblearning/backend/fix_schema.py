file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/user.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Add role and contact_email to UserUpdate if they are missing
if "role: Optional[str] = None" not in content:
    content = content.replace(
        "class UserUpdate(BaseModel):\n    full_name: Optional[str] = None\n    contact_email: Optional[str] = None",
        "class UserUpdate(BaseModel):\n    full_name: Optional[str] = None\n    contact_email: Optional[str] = None\n    role: Optional[str] = None"
    )
    if "class UserUpdate(BaseModel):\n    full_name: Optional[str] = None\n    avatar_url:" in content:
        content = content.replace(
            "class UserUpdate(BaseModel):\n    full_name: Optional[str] = None",
            "class UserUpdate(BaseModel):\n    full_name: Optional[str] = None\n    contact_email: Optional[str] = None\n    role: Optional[str] = None"
        )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated UserUpdate schema to include role and contact_email")
else:
    print("UserUpdate schema already has role")
