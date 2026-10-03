import re

file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFilters.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the placeholder text
content = re.sub(
    r'placeholder="T.m ki.m theo t.n, email\.\.\."',
    'placeholder="Tìm kiếm theo tên, tên đăng nhập..."',
    content
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated search placeholder to username")
