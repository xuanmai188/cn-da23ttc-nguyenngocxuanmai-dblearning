file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/UserManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("new Date(u.created_at).toLocaleDateString", "new Date(u.created_at + (!u.created_at.endsWith('Z') ? 'Z' : '')).toLocaleDateString")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("UserManagement.jsx timezone fixed")
