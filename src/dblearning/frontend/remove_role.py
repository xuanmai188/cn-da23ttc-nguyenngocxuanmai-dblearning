import re

file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFilters.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove the dropdown div using regex
# We match `<div className="flex-1 min-w-[150px] max-w-[250px]">\s*<label.*?</select>\s*</div>`
new_content = re.sub(
    r'<div className="flex-1 min-w-\[150px\] max-w-\[250px\]">\s*<label.*?<\/select>\s*<\/div>',
    '',
    content,
    flags=re.DOTALL
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Removed Vai trò dropdown from UserFilters.jsx")
