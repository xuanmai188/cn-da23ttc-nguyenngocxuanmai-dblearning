file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/learning.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

if "from app.ml.profile_builder import update_user_profile" not in content:
    content = content.replace(
        "from app.schemas.learning import",
        "from app.ml.profile_builder import update_user_profile\nfrom app.schemas.learning import"
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Added import update_user_profile")
else:
    print("Already imported")
