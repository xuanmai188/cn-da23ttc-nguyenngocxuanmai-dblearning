file_path = "D:/DemoCN2026/dblearning/frontend/src/App.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add imports
imports = """import AdminRoute from './components/AdminRoute';
import AdminLayout from './components/AdminLayout';
import AdminDashboard from './pages/admin/AdminDashboard';
import UserManagement from './pages/admin/UserManagement';
"""

content = content.replace("import Layout from './components/Layout';", "import Layout from './components/Layout';\n" + imports)

# Add routes
admin_routes = """
        {/* Admin Routes */}
        <Route path="/admin/dashboard" element={<AdminRoute><AdminLayout><AdminDashboard /></AdminLayout></AdminRoute>} />
        <Route path="/admin/users" element={<AdminRoute><AdminLayout><UserManagement /></AdminLayout></AdminRoute>} />
"""

content = content.replace("{/* Protected Routes */}", admin_routes + "\n        {/* Protected Routes */}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("App.jsx updated")
