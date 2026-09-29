file_path = "D:/DemoCN2026/dblearning/frontend/src/components/Layout.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove the Admin Panel button logic
old_logic = """  if (user?.role === 'admin') {
    navigation.push({ name: 'Quản trị (Admin)', href: '/admin/dashboard', icon: ChartBarIcon });
  }"""

content = content.replace(old_logic, "")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Layout.jsx updated to hide admin button")
