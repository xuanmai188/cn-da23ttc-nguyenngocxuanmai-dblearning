file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/user.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

if "class UserCreate(UserBase):\n    password: str\n    role: str = \"student\"" not in content:
    content = content.replace(
        "class UserCreate(UserBase):\n    password: str\n",
        "class UserCreate(UserBase):\n    password: str\n    role: str = \"student\"\n"
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Added role to UserCreate")
else:
    print("UserCreate already has role")
