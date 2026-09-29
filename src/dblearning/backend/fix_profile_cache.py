file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/recommendation.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import_statement = "from app.ml.profile_builder import update_user_profile"
if import_statement not in content:
    # it's already there on line 9
    pass

new_func = """@router.get("/profile", response_model=LearningProfileSchema)
def get_learning_profile(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    \"\"\"Lấy hồ sơ học tập (Learning Profile) của người dùng.\"\"\"
    # Cập nhật profile để đảm bảo chuỗi học tập (streak) và thống kê luôn chính xác nhất khi load dashboard
    profile = update_user_profile(db, current_user.id)
    return profile"""

import re
content = re.sub(r'@router\.get\("/profile", response_model=LearningProfileSchema\).*?return profile', new_func, content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("recommendation.py updated")
