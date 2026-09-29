file_path = "D:/DemoCN2026/dblearning/frontend/src/components/AdminLayout.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("{ name: 'Nội dung', href: '#', icon: BookOpenIcon },", "{ name: 'Nội dung', href: '/admin/content', icon: BookOpenIcon },")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("AdminLayout updated")
