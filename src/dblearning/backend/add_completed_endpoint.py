import os

file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/learning.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Check if endpoint already exists
if "def get_completed_items" not in content:
    new_endpoint = """
@router.get("/completed-items", response_model=List[int])
def get_completed_items(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    \"\"\"Lấy danh sách ID các bài học đã hoàn thành của user hiện tại.\"\"\"
    completed_sessions = db.query(LearningSession.item_id).filter(
        LearningSession.user_id == current_user.id,
        LearningSession.status == "completed"
    ).all()
    
    # Also add quizzes passed if they are considered "completed" (or maybe session covers it? 
    # Usually quiz creates a session too, but let's check QuizResult to be sure)
    passed_quizzes = db.query(Quiz.item_id).join(QuizResult).filter(
        QuizResult.user_id == current_user.id,
        QuizResult.is_passed == True
    ).all()
    
    item_ids = set([item[0] for item in completed_sessions])
    item_ids.update([item[0] for item in passed_quizzes])
    
    return list(item_ids)
"""
    content += new_endpoint
    # Ensure Quiz, QuizResult are imported
    if "from app.models.models import" in content and "QuizResult" not in content:
        content = content.replace("Recommendation", "Recommendation, Quiz, QuizResult")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Added completed-items endpoint")
else:
    print("completed-items endpoint already exists")
