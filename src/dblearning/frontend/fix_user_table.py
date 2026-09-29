file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/UserManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("<th className=\"px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider\">Học viên</th>", "<th className=\"px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider\">Người dùng</th>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("UserManagement.jsx updated")
