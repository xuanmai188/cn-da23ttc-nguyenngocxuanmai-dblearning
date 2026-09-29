for file_name in ["Register.jsx", "Login.jsx"]:
    file_path = f"D:/DemoCN2026/dblearning/frontend/src/pages/{file_name}"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Change input type from email to text
    content = content.replace("type=\"email\"", "type=\"text\"")
    # Change placeholders
    content = content.replace("placeholder=\"nhap@email.com\"", "placeholder=\"Ten_dang_nhap\"")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Updated Login and Register inputs")
