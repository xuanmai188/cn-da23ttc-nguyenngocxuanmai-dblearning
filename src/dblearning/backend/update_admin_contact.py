import re

file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Update POST /users (create_user)
content = content.replace(
    "phone_number=user_in.phone_number,",
    "phone_number=user_in.phone_number,\n        contact_email=user_in.contact_email,"
)

# Update PUT /users/{id} (update_user)
# We need to find the update logic. Usually it iterates over dict or manually sets.
# Let's check how update is done.
update_logic = """    if user_in.full_name is not None:
        user.full_name = user_in.full_name"""
new_update_logic = """    if user_in.full_name is not None:
        user.full_name = user_in.full_name
    if user_in.contact_email is not None:
        user.contact_email = user_in.contact_email"""

if "user_in.contact_email is not None" not in content:
    content = content.replace(update_logic, new_update_logic)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated admin.py for contact_email")
