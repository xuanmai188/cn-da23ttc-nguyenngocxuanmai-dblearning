import os

file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"

content = """from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from app.api import deps
from app.models.models import User, LearningSession, QuizResult, Topic, LearningProfile, LearningItem, Quiz, Question
from app.schemas.admin import (
    DashboardStats, UserList, UserItem, ChartDataPoint, TopicAdminResponse, TopicCreateUpdate,
    TopicLearningStat, PerformanceStat, ActiveStudent, PopularLesson, RecentActivity
)
from typing import List

router = APIRouter()

@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    # Card 1: Users
    total_users = db.query(User).count()
    total_students = db.query(User).filter(User.role == "student").count()
    total_admins = db.query(User).filter(User.role == "admin").count()
    
    # Card 2: Content
    total_learning_items = db.query(LearningItem).count()
    total_topics = db.query(Topic).count()
    
    # Card 3: Quizzes
    total_quizzes = db.query(Quiz).count()
    total_questions = db.query(Question).count()
    
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
        "user_growth_rate": 12.0, # Mock growth rate for now
        "total_learning_items": total_learning_items,
        "total_topics": total_topics,
        "item_growth_rate": 8.0,
        "total_quizzes": total_quizzes,
        "total_questions": total_questions,
        "quiz_growth_rate": 15.0,
        "today_sessions": today_sessions,
        "yesterday_sessions": yesterday_sessions,
        "session_growth_rate": round(session_growth_rate, 1)
    }

@router.get("/charts/topic-learning", response_model=List[TopicLearningStat])
def get_topic_learning_stats(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    results = db.query(
        Topic.name,
        Topic.color,
        func.count(LearningSession.id).label('sessions')
    ).join(LearningItem, LearningItem.topic_id == Topic.id) \\
     .join(LearningSession, LearningSession.item_id == LearningItem.id) \\
     .group_by(Topic.id) \\
     .order_by(desc('sessions')) \\
     .all()
    
    return [{"name": r.name, "color": r.color, "sessions": r.sessions} for r in results]

@router.get("/performance", response_model=PerformanceStat)
def get_performance_stats(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    # Calculate global completion rate (completed sessions / total sessions)
    total_sessions = db.query(LearningSession).count()
    completed_sessions = db.query(LearningSession).filter(LearningSession.status == "completed").count()
    completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
    
    # Calculate avg quiz score
    avg_quiz_score = db.query(func.avg(QuizResult.score)).scalar() or 0.0
    
    # Mock some data for the other two rates since we don't track them distinctly enough yet
    return {
        "completion_rate": round(completion_rate, 1),
        "avg_quiz_score": round(avg_quiz_score, 1),
        "quiz_attempt_rate": 55.0,
        "document_view_rate": 81.0
    }

@router.get("/active-students", response_model=List[ActiveStudent])
def get_active_students(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    profiles = db.query(
        User.id,
        User.full_name,
        LearningProfile.total_items_completed,
        LearningProfile.total_quizzes_taken,
        LearningProfile.avg_quiz_score,
        LearningProfile.total_study_hours
    ).join(LearningProfile, User.id == LearningProfile.user_id) \\
     .filter(User.role == "student") \\
     .order_by(desc(LearningProfile.total_items_completed)) \\
     .limit(5).all()
     
    return [
        {
            "id": p.id,
            "full_name": p.full_name,
            "completed_items": p.total_items_completed,
            "quizzes_taken": p.total_quizzes_taken,
            "avg_score": round(p.avg_quiz_score, 1),
            "total_hours": round(p.total_study_hours, 1)
        } for p in profiles
    ]

@router.get("/popular-lessons", response_model=List[PopularLesson])
def get_popular_lessons(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    lessons = db.query(
        LearningItem.id,
        LearningItem.title,
        Topic.name.label('topic_name'),
        LearningItem.view_count,
        func.count(LearningSession.id).label('sessions')
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
            "completion_rate": 80.0 # Mock completion rate for now
        } for l in lessons
    ]

@router.get("/recent-activities", response_model=List[RecentActivity])
def get_recent_activities(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    # Since we don't have a dedicated activities table, we mock this for now based on recent sessions
    recent_sessions = db.query(
        LearningSession.id,
        User.full_name,
        LearningItem.title,
        LearningItem.content_type,
        LearningSession.started_at
    ).join(User, LearningSession.user_id == User.id) \\
     .join(LearningItem, LearningSession.item_id == LearningItem.id) \\
     .order_by(desc(LearningSession.started_at)) \\
     .limit(5).all()
     
    activities = []
    for s in recent_sessions:
        action = "đang xem"
        if s.content_type == "quiz": action = "đang làm"
        
        # Simple time ago string (mocked to minutes for UI demo)
        delta = datetime.utcnow() - s.started_at
        mins_ago = int(delta.total_seconds() / 60)
        time_str = f"{mins_ago} phút trước" if mins_ago < 60 else f"{mins_ago // 60} giờ trước"
        
        activities.append({
            "id": s.id,
            "user_name": s.full_name,
            "action": action,
            "target": s.title,
            "time_ago": time_str,
            "type": s.content_type
        })
    return activities

@router.get("/users", response_model=UserList)
def get_users(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    users = db.query(User).order_by(User.id.desc()).all()
    return {
        "users": users,
        "total": len(users)
    }

@router.put("/users/{user_id}/status")
def toggle_user_status(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == current_admin.id:
        raise HTTPException(status_code=400, detail="Cannot block yourself")
        
    user.is_active = not user.is_active
    db.commit()
    
    status_str = "unblocked" if user.is_active else "blocked"
    return {"message": f"User {user_id} {status_str} successfully"}

@router.put("/users/{user_id}/role")
def toggle_user_role(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user.id == current_admin.id:
        raise HTTPException(status_code=400, detail="Cannot change your own role")
        
    user.role = "admin" if user.role == "student" else "student"
    db.commit()
    
    return {"message": f"User {user_id} role changed to {user.role}"}

@router.get("/charts/user-growth", response_model=List[ChartDataPoint])
def get_user_growth(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    results = db.query(
        func.date(User.created_at).label('date'),
        func.count(User.id).label('count')
    ).filter(User.created_at >= thirty_days_ago).group_by(func.date(User.created_at)).all()
    return [{"date": str(r.date), "count": r.count} for r in results]

@router.get("/charts/activity", response_model=List[ChartDataPoint])
def get_activity_chart(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    results = db.query(
        func.date(QuizResult.taken_at).label('date'),
        func.count(QuizResult.id).label('count')
    ).filter(QuizResult.taken_at >= thirty_days_ago).group_by(func.date(QuizResult.taken_at)).all()
    return [{"date": str(r.date), "count": r.count} for r in results]

@router.get("/topics", response_model=List[TopicAdminResponse])
def get_admin_topics(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    topics = db.query(Topic).order_by(Topic.order_index).all()
    res = []
    for t in topics:
        res.append({
            "id": t.id,
            "name": t.name,
            "slug": t.slug,
            "description": t.description,
            "item_count": len(t.learning_items),
            "is_active": t.is_active
        })
    return res

@router.post("/topics", response_model=TopicAdminResponse)
def create_topic(
    topic_in: TopicCreateUpdate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    db_topic = Topic(
        name=topic_in.name,
        slug=topic_in.slug,
        description=topic_in.description,
        is_active=topic_in.is_active,
        order_index=0
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return {
        "id": db_topic.id,
        "name": db_topic.name,
        "slug": db_topic.slug,
        "description": db_topic.description,
        "item_count": 0,
        "is_active": db_topic.is_active
    }

@router.put("/topics/{topic_id}", response_model=TopicAdminResponse)
def update_topic(
    topic_id: int,
    topic_in: TopicCreateUpdate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")
        
    db_topic.name = topic_in.name
    db_topic.slug = topic_in.slug
    db_topic.description = topic_in.description
    db_topic.is_active = topic_in.is_active
    db.commit()
    db.refresh(db_topic)
    
    return {
        "id": db_topic.id,
        "name": db_topic.name,
        "slug": db_topic.slug,
        "description": db_topic.description,
        "item_count": len(db_topic.learning_items),
        "is_active": db_topic.is_active
    }

@router.delete("/topics/{topic_id}")
def delete_topic(
    topic_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    db_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not db_topic:
        raise HTTPException(status_code=404, detail="Topic not found")
        
    if len(db_topic.learning_items) > 0:
        raise HTTPException(status_code=400, detail="Cannot delete topic with existing items")
        
    db.delete(db_topic)
    db.commit()
    return {"message": "Topic deleted successfully"}
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated admin.py endpoints")
