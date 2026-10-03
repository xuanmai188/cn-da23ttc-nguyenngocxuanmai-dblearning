file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFilters.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target = "Tìm kiếm theo tên, tên đăng nhập..."
replacement = "Tìm kiếm theo tên, email..."

if target in content:
    content = content.replace(target, replacement)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replaced placeholder text successfully")
else:
    print("Target not found")
