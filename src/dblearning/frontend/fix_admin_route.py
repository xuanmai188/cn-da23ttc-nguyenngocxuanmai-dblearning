file_path = "D:/DemoCN2026/dblearning/frontend/src/components/AdminRoute.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("'admin@dblearning.edu.vn'", "'admin'")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed auto-login in AdminRoute.jsx")
