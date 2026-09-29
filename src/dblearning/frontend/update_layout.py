file_path = "D:/DemoCN2026/dblearning/frontend/src/components/Layout.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add Admin Panel to the navigation
nav_item = """  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: ChartBarIcon },
    { name: 'Chủ đề', href: '/topics', icon: BookOpenIcon },
    { name: 'Lộ trình của tôi', href: '/my-path', icon: MapIcon },
    { name: 'Cài đặt', href: '/settings', icon: Cog6ToothIcon },
  ];
  
  if (user?.role === 'admin') {
    navigation.push({ name: 'Quản trị (Admin)', href: '/admin/dashboard', icon: ChartBarIcon });
  }
"""

content = content.replace("  const navigation = [\n    { name: 'Dashboard', href: '/dashboard', icon: ChartBarIcon },\n    { name: 'Chủ đề', href: '/topics', icon: BookOpenIcon },\n    { name: 'Lộ trình của tôi', href: '/my-path', icon: MapIcon },\n    { name: 'Cài đặt', href: '/settings', icon: Cog6ToothIcon },\n  ];", nav_item)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Layout.jsx updated")
