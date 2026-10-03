import sys
file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
if "delete_user" in content or "@router.delete(\"/users/" in content:
    print("Delete endpoint exists")
else:
    print("No delete endpoint for users")
