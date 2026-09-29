file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/ForgotPassword.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("setMessage(response.data.message);", "setMessage(response.message);")
content = content.replace("if (response.data.debug_reset_link) {", "if (response.debug_reset_link) {")
content = content.replace("setDebugLink(response.data.debug_reset_link);", "setDebugLink(response.debug_reset_link);")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("ForgotPassword.jsx fixed")
