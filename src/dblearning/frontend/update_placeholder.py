import re

file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFilters.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the placeholder text. We'll use a regex that ignores encoding issues with "Tìm kiếm theo tên, email, MSSV..."
content = re.sub(
    r'placeholder="T.m ki.m theo t.n, email, MSSV\.\.\."',
    'placeholder="Tìm kiếm theo tên, email..."',
    content
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated search placeholder")
