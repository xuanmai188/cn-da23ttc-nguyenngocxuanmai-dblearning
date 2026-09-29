file_path = "D:/DemoCN2026/dblearning/backend/app/ml/profile_builder.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import_statement = "from app.models.models import LearningSession, QuizResult, LearningProfile, Topic, LearningItem"

new_code = """    # Nếu user chưa có lịch sử học nhưng đã làm khảo sát (onboarded), giữ nguyên profile
    profile = db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()
    if profile and profile.is_onboarded and len(sessions) == 0 and len(quiz_results) == 0:
        profile.learning_streak = 0
        db.commit()
        return profile"""

# Insert right after: quiz_results = db.query(QuizResult).filter(QuizResult.user_id == user_id).all()
content = content.replace(
    "quiz_results = db.query(QuizResult).filter(QuizResult.user_id == user_id).all()",
    "quiz_results = db.query(QuizResult).filter(QuizResult.user_id == user_id).all()\n\n" + new_code
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("profile_builder.py updated")
