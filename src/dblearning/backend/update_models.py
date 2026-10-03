import re
import sys

# Update models.py
models_path = "D:/DemoCN2026/dblearning/backend/app/models/models.py"
with open(models_path, "r", encoding="utf-8") as f:
    models_content = f.read()

if "contact_email =" not in models_content:
    models_content = models_content.replace(
        "full_name = Column(String(255), nullable=False)",
        "full_name = Column(String(255), nullable=False)\n    contact_email = Column(String(255), nullable=True)"
    )
    with open(models_path, "w", encoding="utf-8") as f:
        f.write(models_content)
    print("Updated models.py")

# Update schemas/user.py
schemas_path = "D:/DemoCN2026/dblearning/backend/app/schemas/user.py"
with open(schemas_path, "r", encoding="utf-8") as f:
    schemas_content = f.read()

if "contact_email: Optional[str] = None" not in schemas_content:
    # Update UserBase
    schemas_content = schemas_content.replace(
        "full_name: Optional[str] = None",
        "full_name: Optional[str] = None\n    contact_email: Optional[str] = None"
    )
    # Update UserCreate
    schemas_content = schemas_content.replace(
        "full_name: str",
        "full_name: str\n    contact_email: Optional[str] = None"
    )
    with open(schemas_path, "w", encoding="utf-8") as f:
        f.write(schemas_content)
    print("Updated schemas/user.py")
