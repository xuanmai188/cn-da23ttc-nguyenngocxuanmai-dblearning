file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/auth.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target = """    if user_in.phone_number is not None:
        current_user.phone_number = user_in.phone_number"""

replacement = """    if user_in.phone_number is not None:
        current_user.phone_number = user_in.phone_number
    if user_in.contact_email is not None:
        current_user.contact_email = user_in.contact_email"""

if target in content:
    content = content.replace(target, replacement)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated update_user_me in auth.py")
else:
    print("Target not found")
