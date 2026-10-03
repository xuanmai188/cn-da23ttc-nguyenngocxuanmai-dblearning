import re

file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target = """    user.full_name = user_in.full_name
    user.phone_number = user_in.phone_number
    user.role = user_in.role"""

replacement = """    user.full_name = user_in.full_name
    user.phone_number = user_in.phone_number
    user.role = user_in.role
    user.contact_email = user_in.contact_email"""

if target in content and "user.contact_email = user_in.contact_email" not in content:
    content = content.replace(target, replacement)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully updated admin.py to save contact_email!")
else:
    print("Could not find target block or it's already updated.")
