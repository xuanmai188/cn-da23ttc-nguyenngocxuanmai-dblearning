file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target = """        user_dict = {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": u.created_at,
            "last_activity_at": last_activity
        }"""

replacement = """        user_dict = {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "phone_number": u.phone_number,
            "contact_email": u.contact_email,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": u.created_at,
            "last_activity_at": last_activity
        }"""

if target in content:
    content = content.replace(target, replacement)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully added phone_number and contact_email to user_dict")
else:
    print("Target not found!")
