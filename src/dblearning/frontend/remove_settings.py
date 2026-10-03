import re
file_path = "D:/DemoCN2026/dblearning/frontend/src/components/AdminLayout.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove the line containing /admin/settings
lines = content.split('\n')
new_lines = [line for line in lines if "'/admin/settings'" not in line]
new_content = '\n'.join(new_lines)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Removed Settings from AdminLayout")
