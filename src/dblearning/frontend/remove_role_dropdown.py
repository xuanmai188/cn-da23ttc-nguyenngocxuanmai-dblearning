file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFilters.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re
# Remove the Vai trò dropdown div
content = re.sub(r'<div className="flex-1 min-w-\[150px\] max-w-\[200px\]">\s*<label className="block text-xs font-medium text-slate-500 mb-1\.5">Vai trò<\/label>\s*<select[^>]*value=\{filters\.role\}[^>]*>\s*<option value="all">Tất cả<\/option>\s*<option value="student">Sinh viên<\/option>\s*<option value="admin">Quản trị viên<\/option>\s*<\/select>\s*<\/div>', "", content)

# Adjust remaining dropdown widths
content = content.replace('max-w-[200px]', 'max-w-[250px]')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Removed Role dropdown from UserFilters.jsx")
