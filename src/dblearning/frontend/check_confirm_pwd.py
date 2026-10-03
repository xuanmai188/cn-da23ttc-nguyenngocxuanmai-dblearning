import sys

files = ["D:/DemoCN2026/dblearning/frontend/src/pages/Register.jsx",
         "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFormModal.jsx"]

for file_path in files:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "confirm_password" in content:
                print(f"{file_path} ALREADY has confirm_password")
            else:
                print(f"{file_path} DOES NOT have confirm_password")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
