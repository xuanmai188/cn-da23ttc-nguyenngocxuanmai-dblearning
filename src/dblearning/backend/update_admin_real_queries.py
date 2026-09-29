import os
import re

file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace get_dashboard_stats mock rates
new_dashboard = """@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    # Card 1: Users
    total_users = db.query(User).count()
    total_students = db.query(User).filter(User.role == "student").count()
    total_admins = db.query(User).filter(User.role == "admin").count()
    
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    sixty_days_ago = datetime.utcnow() - timedelta(days=60)
    
    users_last_30 = db.query(User).filter(User.created_at >= thirty_days_ago).count()
    users_prev_30 = db.query(User).filter(User.created_at >= sixty_days_ago, User.created_at < thirty_days_ago).count()
    user_growth_rate = ((users_last_30 - users_prev_30) / users_prev_30 * 100) if users_prev_30 > 0 else (100.0 if users_last_30 > 0 else 0.0)
    
    # Card 2: Content
    total_learning_items = db.query(LearningItem).count()
    total_topics = db.query(Topic).count()
    
    items_last_30 = db.query(LearningItem).filter(LearningItem.created_at >= thirty_days_ago).count()
    items_prev_30 = db.query(LearningItem).filter(LearningItem.created_at >= sixty_days_ago, LearningItem.created_at < thirty_days_ago).count()
    item_growth_rate = ((items_last_30 - items_prev_30) / items_prev_30 * 100) if items_prev_30 > 0 else (100.0 if items_last_30 > 0 else 0.0)
    
    # Card 3: Quizzes
    total_quizzes = db.query(Quiz).count()
    total_questions = db.query(Question).count()
    
    quizzes_last_30 = db.query(Quiz).filter(Quiz.created_at >= thirty_days_ago).count()
    quizzes_prev_30 = db.query(Quiz).filter(Quiz.created_at >= sixty_days_ago, Quiz.created_at < thirty_days_ago).count()
    quiz_growth_rate = ((quizzes_last_30 - quizzes_prev_30) / quizzes_prev_30 * 100) if quizzes_prev_30 > 0 else (100.0 if quizzes_last_30 > 0 else 0.0)
    
    # Card 4: Sessions Today vs Yesterday
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    
    today_sessions = db.query(LearningSession).filter(
        func.date(LearningSession.started_at) == today
    ).count()
    
    yesterday_sessions = db.query(LearningSession).filter(
        func.date(LearningSession.started_at) == yesterday
    ).count()
    
    session_growth_rate = 0.0
    if yesterday_sessions > 0:
        session_growth_rate = ((today_sessions - yesterday_sessions) / yesterday_sessions) * 100
    elif today_sessions > 0:
        session_growth_rate = 100.0

    return {
        "total_users": total_users,
        "total_students": total_students,
        "total_admins": total_admins,
        "user_growth_rate": round(user_growth_rate, 1),
        "total_learning_items": total_learning_items,
        "total_topics": total_topics,
        "item_growth_rate": round(item_growth_rate, 1),
        "total_quizzes": total_quizzes,
        "total_questions": total_questions,
        "quiz_growth_rate": round(quiz_growth_rate, 1),
        "today_sessions": today_sessions,
        "yesterday_sessions": yesterday_sessions,
        "session_growth_rate": round(session_growth_rate, 1)
    }"""
content = re.sub(r'@router\.get\("/dashboard".*?return \{.*?\n    \}', new_dashboard, content, flags=re.DOTALL)


# Replace performance stats
new_performance = """@router.get("/performance", response_model=PerformanceStat)
def get_performance_stats(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    total_sessions = db.query(LearningSession).count()
    completed_sessions = db.query(LearningSession).filter(LearningSession.status == "completed").count()
    completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
    
    avg_quiz_score = db.query(func.avg(QuizResult.score)).scalar() or 0.0
    
    quiz_sessions = db.query(LearningSession).join(LearningItem).filter(LearningItem.content_type == 'quiz').count()
    doc_sessions = db.query(LearningSession).join(LearningItem).filter(LearningItem.content_type == 'document').count()
    
    quiz_attempt_rate = (quiz_sessions / total_sessions * 100) if total_sessions > 0 else 0
    document_view_rate = (doc_sessions / total_sessions * 100) if total_sessions > 0 else 0
    
    return {
        "completion_rate": round(completion_rate, 1),
        "avg_quiz_score": round(avg_quiz_score, 1),
        "quiz_attempt_rate": round(quiz_attempt_rate, 1),
        "document_view_rate": round(document_view_rate, 1)
    }"""
content = re.sub(r'@router\.get\("/performance".*?return \{.*?\n    \}', new_performance, content, flags=re.DOTALL)


# Replace popular lessons
new_popular = """@router.get("/popular-lessons", response_model=List[PopularLesson])
def get_popular_lessons(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    lessons = db.query(
        LearningItem.id,
        LearningItem.title,
        Topic.name.label('topic_name'),
        LearningItem.view_count,
        func.avg(LearningSession.completion_rate).label('avg_completion')
    ).join(Topic, LearningItem.topic_id == Topic.id) \\
     .outerjoin(LearningSession, LearningSession.item_id == LearningItem.id) \\
     .group_by(LearningItem.id) \\
     .order_by(desc(LearningItem.view_count)) \\
     .limit(5).all()
     
    return [
        {
            "id": l.id,
            "title": l.title,
            "topic_name": l.topic_name,
            "view_count": l.view_count,
            "completion_rate": round((l.avg_completion or 0) * 100, 1)
        } for l in lessons
    ]"""
content = re.sub(r'@router\.get\("/popular-lessons".*?return \[.*?\]', new_popular, content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated admin.py with 100% real queries")
