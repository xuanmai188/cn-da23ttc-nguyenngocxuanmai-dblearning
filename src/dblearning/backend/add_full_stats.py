file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_endpoint = """
# --- Full Statistics ---
@router.get("/statistics/full")
def get_full_statistics(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    now = datetime.utcnow()
    seven_days_ago = now - timedelta(days=7)
    
    # 1. Overview KPIs
    total_users = db.query(User).count()
    
    # Active users: Has a learning session in the last 7 days
    active_users = db.query(LearningSession.user_id).filter(LearningSession.started_at >= seven_days_ago).distinct().count()
    
    total_items = db.query(LearningItemModel).count()
    
    avg_quiz_score = db.query(func.avg(QuizResult.score)).scalar() or 0.0
    
    # 2. User Structure
    students = db.query(User).filter(User.role == "student").count()
    admins = db.query(User).filter(User.role == "admin").count()
    blocked = db.query(User).filter(User.is_active == False).count()
    
    # 3. Performance Stats
    total_sessions = db.query(LearningSession).count()
    completed_sessions = db.query(LearningSession).filter(LearningSession.status == "completed").count()
    completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0.0
    
    quiz_sessions = db.query(LearningSession).join(LearningItemModel).filter(LearningItemModel.content_type == 'quiz').count()
    doc_sessions = db.query(LearningSession).join(LearningItemModel).filter(LearningItemModel.content_type == 'document').count()
    
    quiz_attempt_rate = (quiz_sessions / total_sessions * 100) if total_sessions > 0 else 0.0
    document_view_rate = (doc_sessions / total_sessions * 100) if total_sessions > 0 else 0.0
    
    # 4. Content Distribution
    docs = db.query(LearningItemModel).filter(LearningItemModel.content_type == 'document').count()
    videos = db.query(LearningItemModel).filter(LearningItemModel.content_type == 'video').count()
    quizzes = db.query(LearningItemModel).filter(LearningItemModel.content_type == 'quiz').count()
    flashcards = db.query(LearningItemModel).filter(LearningItemModel.content_type == 'flashcard_set').count()
    
    # 5. Recommendation Effectiveness
    # (Assuming Recommendation model is imported, it should be if models.py is imported as a whole)
    from app.models.models import Recommendation
    total_recs = db.query(Recommendation).count()
    clicked_recs = db.query(Recommendation).filter(Recommendation.is_clicked == True).count()
    click_rate = (clicked_recs / total_recs * 100) if total_recs > 0 else 0.0
    
    # Completed recommended items
    # Join Recommendation with LearningSession on user_id and item_id
    completed_recs = db.query(Recommendation).join(
        LearningSession, 
        (Recommendation.user_id == LearningSession.user_id) & (Recommendation.item_id == LearningSession.item_id)
    ).filter(
        Recommendation.is_clicked == True,
        LearningSession.status == "completed"
    ).count()
    
    completion_rate_recs = (completed_recs / clicked_recs * 100) if clicked_recs > 0 else 0.0
    
    return {
        "overview": {
            "total_users": total_users,
            "active_users": active_users,
            "total_items": total_items,
            "avg_quiz_score": round(avg_quiz_score, 1)
        },
        "users": {
            "students": students,
            "admins": admins,
            "blocked": blocked
        },
        "performance": {
            "completion_rate": round(completion_rate, 1),
            "avg_quiz_score": round(avg_quiz_score, 1),
            "quiz_attempt_rate": round(quiz_attempt_rate, 1),
            "document_view_rate": round(document_view_rate, 1)
        },
        "content_distribution": {
            "document": docs,
            "video": videos,
            "quiz": quizzes,
            "flashcard_set": flashcards
        },
        "recommendations": {
            "total": total_recs,
            "clicked": clicked_recs,
            "click_rate": round(click_rate, 1),
            "completed": completed_recs,
            "completion_rate": round(completion_rate_recs, 1)
        }
    }
"""

content = content + new_endpoint

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Added /statistics/full endpoint to admin.py")
