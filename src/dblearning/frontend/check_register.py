file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/auth/Register.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if "formData" in line or "handleSubmit" in line or "full_name" in line:
            print(f"{i}: {line.strip()}")
