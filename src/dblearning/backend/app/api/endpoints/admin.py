from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from app.api import deps
from app.models.models import User, LearningSession, QuizResult, Topic, LearningProfile, LearningItem, Quiz, Question
from app.schemas.admin import (
    DashboardStats, UserList, UserItem, ChartDataPoint, TopicAdminResponse, TopicCreateUpdate,
    TopicLearningStat, PerformanceStat, ActiveStudent, PopularLesson, RecentActivity,
    UserStats, UserDetailResponse, UserHistoryResponse
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
    ).join(LearningItem, LearningItem.topic_id == Topic.id) \
     .join(LearningSession, LearningSession.item_id == LearningItem.id) \
     .group_by(Topic.id) \
     .order_by(desc('sessions')) \
     .all()
    
    return [{"name": r.name, "color": r.color, "sessions": r.sessions} for r in results]

@router.get("/performance", response_model=PerformanceStat)
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
    ).join(LearningProfile, User.id == LearningProfile.user_id) \
     .filter(User.role == "student") \
     .order_by(desc(LearningProfile.total_items_completed)) \
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
        func.avg(LearningSession.completion_rate).label('avg_completion')
    ).join(Topic, LearningItem.topic_id == Topic.id) \
     .outerjoin(LearningSession, LearningSession.item_id == LearningItem.id) \
     .group_by(LearningItem.id) \
     .order_by(desc(LearningItem.view_count)) \
     .limit(5).all()
     
    return [
        {
            "id": l.id,
            "title": l.title,
            "topic_name": l.topic_name,
            "view_count": l.view_count,
            "completion_rate": round((l.avg_completion or 0) * 100, 1)
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
    ).join(User, LearningSession.user_id == User.id) \
     .join(LearningItem, LearningSession.item_id == LearningItem.id) \
     .order_by(desc(LearningSession.started_at)) \
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

@router.get("/users/stats")
def get_user_stats(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    total = db.query(User).count()
    students = db.query(User).filter(User.role == "student").count()
    admins = db.query(User).filter(User.role == "admin").count()
    blocked = db.query(User).filter(User.is_active == False).count()
    
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    sixty_days_ago = datetime.utcnow() - timedelta(days=60)
    users_last_30 = db.query(User).filter(User.created_at >= thirty_days_ago).count()
    users_prev_30 = db.query(User).filter(User.created_at >= sixty_days_ago, User.created_at < thirty_days_ago).count()
    growth_rate = ((users_last_30 - users_prev_30) / users_prev_30 * 100) if users_prev_30 > 0 else (100.0 if users_last_30 > 0 else 0.0)
    
    return {
        "total": total,
        "students": students,
        "admins": admins,
        "blocked": blocked,
        "growth_rate": round(growth_rate, 1),
        "student_rate": round((students / total * 100) if total > 0 else 0, 1),
        "admin_rate": round((admins / total * 100) if total > 0 else 0, 1),
        "blocked_rate": round((blocked / total * 100) if total > 0 else 0, 1)
    }

from typing import Optional

@router.get("/users", response_model=UserList)
def get_users(
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    role: Optional[str] = None,
    status: Optional[str] = None,
    date: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    query = db.query(User)
    
    if search:
        search = f"%{search}%"
        query = query.filter(
            (User.full_name.ilike(search)) | (User.email.ilike(search))
        )
    
    if role and role != "all":
        query = query.filter(User.role == role)
        
    if status and status != "all":
        is_active = True if status == "active" else False
        query = query.filter(User.is_active == is_active)
        
    if date and date != "all":
        now = datetime.utcnow()
        if date == "7days":
            query = query.filter(User.created_at >= now - timedelta(days=7))
        elif date == "30days":
            query = query.filter(User.created_at >= now - timedelta(days=30))
        elif date == "3months":
            query = query.filter(User.created_at >= now - timedelta(days=90))
            
    total = query.count()
    users = query.order_by(User.id.desc()).offset((page - 1) * limit).limit(limit).all()
    
    # Enrich with last_activity_at
    enriched_users = []
    for u in users:
        # Get latest session
        latest_session = db.query(LearningSession.started_at).filter(LearningSession.user_id == u.id).order_by(desc(LearningSession.started_at)).first()
        last_activity = None
        if latest_session:
            # Format time ago
            delta = datetime.utcnow() - latest_session[0]
            mins = int(delta.total_seconds() / 60)
            if mins < 60:
                last_activity = f"{mins} phút trước"
            elif mins < 1440:
                last_activity = f"{mins // 60} giờ trước"
            else:
                last_activity = f"{mins // 1440} ngày trước"
        
        user_dict = {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": u.created_at,
            "last_activity_at": last_activity
        }
        enriched_users.append(user_dict)

    return {
        "users": enriched_users,
        "total": total
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

@router.get("/users/{user_id}/details", response_model=UserDetailResponse)
def get_user_details(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    latest_session = db.query(LearningSession.started_at).filter(LearningSession.user_id == user.id).order_by(desc(LearningSession.started_at)).first()
    last_activity = None
    if latest_session:
        delta = datetime.utcnow() - latest_session[0]
        mins = int(delta.total_seconds() / 60)
        if mins < 60:
            last_activity = f"{mins} phút trước"
        elif mins < 1440:
            last_activity = f"{mins // 60} giờ trước"
        else:
            last_activity = f"{mins // 1440} ngày trước"
            
    profile = db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()
    
    stats = {
        "completed_lessons": profile.total_items_completed if profile else 0,
        "taken_quizzes": profile.total_quizzes_taken if profile else 0,
        "avg_score": round(profile.avg_quiz_score, 1) if profile else 0.0,
        "total_hours": round(profile.total_study_hours, 1) if profile else 0.0
    }
    
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "phone_number": user.phone_number,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "last_activity_at": last_activity,
        "stats": stats
    }

@router.get("/users/{user_id}/history", response_model=UserHistoryResponse)
def get_user_history(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    sessions = db.query(
        LearningSession.id,
        LearningSession.started_at,
        LearningSession.status,
        LearningItem.title,
        LearningItem.content_type
    ).join(LearningItem, LearningSession.item_id == LearningItem.id) \
     .filter(LearningSession.user_id == user_id) \
     .order_by(desc(LearningSession.started_at)) \
     .limit(20).all()
     
    history = []
    for s in sessions:
        action = "Hoàn thành" if s.status == "completed" else "Đang học"
        if s.content_type == "quiz":
            action = "Hoàn thành bài Test" if s.status == "completed" else "Đang làm bài Test"
        elif s.content_type == "document":
            action = "Đã xem tài liệu" if s.status == "completed" else "Đang đọc tài liệu"
            
        delta = datetime.utcnow() - s.started_at
        mins = int(delta.total_seconds() / 60)
        time_ago = f"{mins} phút trước" if mins < 60 else (f"{mins // 60} giờ trước" if mins < 1440 else f"{mins // 1440} ngày trước")
        
        history.append({
            "id": s.id,
            "action": action,
            "target": s.title,
            "target_type": s.content_type,
            "created_at": s.started_at,
            "time_ago": time_ago
        })
        
    return {"history": history}

from pydantic import BaseModel
from typing import Optional
from app.core.security import get_password_hash

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    phone_number: Optional[str] = None
    role: str = "student"

class UserUpdate(BaseModel):
    full_name: str
    phone_number: Optional[str] = None
    role: str

@router.post("/users")
def create_user(
    user_in: UserCreate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")
    
    new_user = User(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        phone_number=user_in.phone_number,
        role=user_in.role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    return {"message": "Tạo thành công"}

@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
        
    user.full_name = user_in.full_name
    user.phone_number = user_in.phone_number
    user.role = user_in.role
    db.commit()
    return {"message": "Cập nhật thành công"}

@router.put("/users/{user_id}/reset-password")
def reset_user_password(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
        
    user.password_hash = get_password_hash("123456")
    db.commit()
    return {"message": "Mật khẩu đã được đặt lại thành 123456"}
