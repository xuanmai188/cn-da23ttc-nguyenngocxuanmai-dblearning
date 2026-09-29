file_path = "D:/DemoCN2026/dblearning/frontend/src/App.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add imports
imports_to_add = """import RecommendationManagement from './pages/admin/RecommendationManagement';
import OnboardingStats from './pages/admin/OnboardingStats';
import Statistics from './pages/admin/Statistics';
import Reports from './pages/admin/Reports';
import AdminSettings from './pages/admin/AdminSettings';"""
content = content.replace("import ContentManagement from './pages/admin/ContentManagement';", f"import ContentManagement from './pages/admin/ContentManagement';\n{imports_to_add}")

# Add routes
routes_to_add = """        <Route path="/admin/recommendations" element={<AdminRoute><AdminLayout><RecommendationManagement /></AdminLayout></AdminRoute>} />
        <Route path="/admin/onboarding" element={<AdminRoute><AdminLayout><OnboardingStats /></AdminLayout></AdminRoute>} />
        <Route path="/admin/statistics" element={<AdminRoute><AdminLayout><Statistics /></AdminLayout></AdminRoute>} />
        <Route path="/admin/reports" element={<AdminRoute><AdminLayout><Reports /></AdminLayout></AdminRoute>} />
        <Route path="/admin/settings" element={<AdminRoute><AdminLayout><AdminSettings /></AdminLayout></AdminRoute>} />"""
content = content.replace("<Route path=\"/admin/content\" element={<AdminRoute><AdminLayout><ContentManagement /></AdminLayout></AdminRoute>} />", f"<Route path=\"/admin/content\" element={{<AdminRoute><AdminLayout><ContentManagement /></AdminLayout></AdminRoute>}} />\n{routes_to_add}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated App.jsx routes")
