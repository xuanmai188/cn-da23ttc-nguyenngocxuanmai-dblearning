file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/UserManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "setFilters({ search: '', role: 'all', status: 'all', date: 'all' });",
    "setFilters({ search: '', status: 'all', date: 'all' });"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed handleResetFilters")
