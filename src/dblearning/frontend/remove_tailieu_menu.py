file_path = "D:/DemoCN2026/dblearning/frontend/src/components/AdminLayout.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# We want to remove the 'Tài liệu' entry
old_menu_item = "        { name: 'Tài liệu', href: '/admin/content?tab=documents' },"
content = content.replace(old_menu_item, "")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Removed Tài liệu from AdminLayout.jsx")
