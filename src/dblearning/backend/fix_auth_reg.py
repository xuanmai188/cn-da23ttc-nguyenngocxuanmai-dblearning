file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/auth.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target = """    user = User(
        email=user_in.email,
        password_hash=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        avatar_url=user_in.avatar_url,
    )"""

replacement = """    user = User(
        email=user_in.email,
        password_hash=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        phone_number=user_in.phone_number,
        contact_email=user_in.contact_email,
        avatar_url=user_in.avatar_url,
    )"""

if target in content:
    content = content.replace(target, replacement)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated auth.py to save phone_number and contact_email")
else:
    print("Target not found in auth.py")
