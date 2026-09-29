file_path = "D:/DemoCN2026/dblearning/backend/app/models/models.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

if "phone_number = Column(String(20), nullable=True)" not in content:
    content = content.replace(
        "full_name = Column(String(255), nullable=False)",
        "full_name = Column(String(255), nullable=False)\n    phone_number = Column(String(20), nullable=True)"
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("models.py updated")
else:
    print("models.py already has phone_number")
