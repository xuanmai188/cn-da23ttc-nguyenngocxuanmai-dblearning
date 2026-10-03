import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFormModal.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    if "is_active" in f.read():
        print("is_active is handled in UserFormModal")
    else:
        print("is_active is NOT in UserFormModal")
