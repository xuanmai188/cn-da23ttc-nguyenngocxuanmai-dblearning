file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/UserManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "}, [page, limit, filters]);",
    "}, [page, limit, filters, activeTab]);"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Added activeTab to useCallback dependencies")
