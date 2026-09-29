file_path = "D:/DemoCN2026/dblearning/frontend/src/App.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "import UserManagement from './pages/admin/UserManagement';",
    "import UserManagement from './pages/admin/UserManagement';\nimport ContentManagement from './pages/admin/ContentManagement';"
)

content = content.replace(
    '<Route path="/admin/users" element={<AdminRoute><AdminLayout><UserManagement /></AdminLayout></AdminRoute>} />',
    '<Route path="/admin/users" element={<AdminRoute><AdminLayout><UserManagement /></AdminLayout></AdminRoute>} />\n        <Route path="/admin/content" element={<AdminRoute><AdminLayout><ContentManagement /></AdminLayout></AdminRoute>} />'
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("App.jsx updated with /admin/content")
