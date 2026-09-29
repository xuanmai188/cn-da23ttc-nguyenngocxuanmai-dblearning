file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/learning.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add Quiz and QuizResult to imports
if "QuizResult" not in content:
    content = content.replace(
        "from app.models.models import Topic, LearningItem, LearningSession, User, Recommendation", 
        "from app.models.models import Topic, LearningItem, LearningSession, User, Recommendation, Quiz, QuizResult"
    )
    # If the original was different:
    if "Topic, LearningItem, LearningSession, User, Recommendation" not in content:
        content = content.replace("from app.models.models import", "from app.models.models import Quiz, QuizResult,")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed imports in learning.py")
else:
    print("Already imported?")
