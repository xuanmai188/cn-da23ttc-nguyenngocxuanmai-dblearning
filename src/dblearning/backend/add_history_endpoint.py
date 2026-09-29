import os

file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/quiz.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Check if endpoint already exists
if "def get_quiz_history_by_item" not in content:
    new_endpoint = """
@router.get("/item/{item_id}/history", response_model=List[QuizResultSchema])
def get_quiz_history_by_item(
    item_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    \"\"\"Lấy lịch sử làm bài kiểm tra của một học liệu.\"\"\"
    quiz = db.query(Quiz).filter(Quiz.item_id == item_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài kiểm tra")
    
    results = db.query(QuizResult).filter(
        QuizResult.quiz_id == quiz.id,
        QuizResult.user_id == current_user.id
    ).order_by(desc(QuizResult.taken_at)).all()
    
    return results
"""
    # Insert it before flashcards or at the end
    content += new_endpoint
    # ensure desc is imported
    if "from sqlalchemy import desc" not in content:
        content = content.replace("from sqlalchemy.orm import Session", "from sqlalchemy.orm import Session\nfrom sqlalchemy import desc")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Added history endpoint")
else:
    print("History endpoint already exists")
