file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFormModal.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
if "confirm_password" in content:
    print("confirm_password logic is present")
else:
    print("confirm_password logic is MISSING")

if "Nhập lại mật khẩu" in content:
    print("Nhập lại mật khẩu UI is present")
else:
    print("Nhập lại mật khẩu UI is MISSING")
