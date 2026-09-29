file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Settings.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("Email đăng nhập", "Tên đăng nhập")
content = content.replace("Email không thể thay đổi để đảm bảo an toàn tài khoản.", "Tên đăng nhập không thể thay đổi để đảm bảo an toàn tài khoản.")
content = content.replace("type=\"email\"", "type=\"text\"")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Settings.jsx")
