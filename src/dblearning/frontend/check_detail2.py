file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserDetailPanel.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
if "Email liên hệ" in content:
    print("Success")
else:
    print("Failed")
