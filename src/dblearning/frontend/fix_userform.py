file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFormModal.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Fix formData
content = content.replace("password: '',\n    contact_email:", "password: '',\n    confirm_password: '',\n    contact_email:")

# Fix confirmPasswordError
if "const [confirmPasswordError" not in content:
    content = content.replace("const [error, setError] = useState('');", "const [error, setError] = useState('');\n  const [confirmPasswordError, setConfirmPasswordError] = useState('');")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed UserFormModal.jsx")
