file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/learning.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "from app.models.models import Topic, LearningItem, LearningSession, User, Recommendation",
    "from app.models.models import Topic, LearningItem, LearningSession, User, Recommendation, Quiz, QuizResult"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Imports fixed properly")
