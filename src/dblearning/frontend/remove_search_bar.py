import re

file_path = "D:/DemoCN2026/dblearning/frontend/src/components/AdminLayout.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Use regex to remove the Search Bar block
content = re.sub(
    r'\s*\{\/\* Search Bar \*\/\}\s*<div className="hidden md:flex items-center max-w-md w-full relative">.*?<\/div>',
    '',
    content,
    flags=re.DOTALL
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Removed Search Bar from AdminLayout.jsx")
