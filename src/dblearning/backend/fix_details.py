file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target = """    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "phone_number": user.phone_number,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "last_activity_at": last_activity,
        "stats": stats
    }"""

replacement = """    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "phone_number": user.phone_number,
        "contact_email": user.contact_email,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "last_activity_at": last_activity,
        "stats": stats
    }"""

if target in content:
    content = content.replace(target, replacement)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully added contact_email to get_user_details")
else:
    print("Target not found")
