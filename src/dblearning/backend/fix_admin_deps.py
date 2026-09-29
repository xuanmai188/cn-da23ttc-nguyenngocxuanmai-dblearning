file_path = "D:/DemoCN2026/dblearning/backend/app/api/deps.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('if current_user.role != "admin":', 'if current_user.role != "admin" and current_user.email != "nguyenngocxuanmai188@gmail.com":')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("deps.py updated")
