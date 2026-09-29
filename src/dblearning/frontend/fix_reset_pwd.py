file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/ResetPassword.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("setMessage(response.data.message);", "setMessage(response.message);")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("ResetPassword.jsx fixed")
