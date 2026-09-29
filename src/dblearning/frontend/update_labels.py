file_path_reg = "D:/DemoCN2026/dblearning/frontend/src/pages/Register.jsx"
with open(file_path_reg, "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace(">Email</label>", ">Tên đăng nhập</label>")
with open(file_path_reg, "w", encoding="utf-8") as f:
    f.write(content)

file_path_login = "D:/DemoCN2026/dblearning/frontend/src/pages/Login.jsx"
with open(file_path_login, "r", encoding="utf-8") as f:
    content_login = f.read()
content_login = content_login.replace(">Email</label>", ">Tên đăng nhập</label>")
with open(file_path_login, "w", encoding="utf-8") as f:
    f.write(content_login)
print("Labels updated")
