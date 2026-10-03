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
from app.schemas.user import UserCreate, UserUpdate

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
    user_growth_rate = users_last_30
    
    # Card 2: Content
    total_learning_items = db.query(LearningItem).count()
    total_topics = db.query(Topic).count()
    
    items_last_30 = db.query(LearningItem).filter(LearningItem.created_at >= thirty_days_ago).count()
    items_prev_30 = db.query(LearningItem).filter(LearningItem.created_at >= sixty_days_ago, LearningItem.created_at < thirty_days_ago).count()
    item_growth_rate = items_last_30
    
    # Card 3: Quizzes
    total_quizzes = db.query(Quiz).count()
    total_questions = db.query(Question).count()
    
    quizzes_last_30 = db.query(Quiz).filter(Quiz.created_at >= thirty_days_ago).count()
    quizzes_prev_30 = db.query(Quiz).filter(Quiz.created_at >= sixty_days_ago, Quiz.created_at < thirty_days_ago).count()
    quiz_growth_rate = quizzes_last_30
    
    # Card 4: Sessions Today vs Yesterday
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    
    today_sessions = db.query(LearningSession).filter(
        func.date(LearningSession.started_at) == today
    ).count()
    
    yesterday_sessions = db.query(LearningSession).filter(
        func.date(LearningSession.started_at) == yesterday
    ).count()
    
    session_growth_rate = today_sessions - yesterday_sessions

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
    limit: int = 5,
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
     .limit(limit).all()
     
    activities = []
    for s in recent_sessions:
        action = "đang xem"
        if s.content_type == "quiz": action = "đang làm"
        
        # Simple time ago string (mocked to minutes for UI demo)
        delta = datetime.utcnow() - s.started_at
        mins_ago = int(delta.total_seconds() / 60)
        time_str = f"{mins_ago} phút trước" if mins_ago < 60 else (f"{mins_ago // 60} giờ trước" if mins_ago < 1440 else f"{mins_ago // 1440} ngày trước")
        
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
    growth_rate = users_last_30
    
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
            "phone_number": u.phone_number,
            "contact_email": u.contact_email,
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
        "contact_email": user.contact_email,
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
        contact_email=user_in.contact_email,
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
        
    update_data = user_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
        
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


from app.models.models import Notification

@router.get("/notifications")
def get_notifications(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    notifications = db.query(Notification).filter(
        Notification.user_id == current_admin.id
    ).order_by(desc(Notification.created_at)).limit(20).all()
    
    unread_count = db.query(Notification).filter(
        Notification.user_id == current_admin.id,
        Notification.is_read == False
    ).count()
    
    return {
        "notifications": notifications,
        "unread_count": unread_count
    }

@router.put("/notifications/read-all")
def mark_all_notifications_read(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    db.query(Notification).filter(
        Notification.user_id == current_admin.id,
        Notification.is_read == False
    ).update({"is_read": True})
    db.commit()
    return {"message": "Đã đánh dấu đọc tất cả"}

@router.put("/notifications/{notif_id}/read")
def mark_notification_read(
    notif_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    notif = db.query(Notification).filter(
        Notification.id == notif_id,
        Notification.user_id == current_admin.id
    ).first()
    if notif:
        notif.is_read = True
        db.commit()
    return {"message": "OK"}

# ==========================================
# LESSONS (ITEMS) MANAGEMENT
# ==========================================
from app.schemas.learning import LearningItem as LearningItemSchema, LearningItemCreate, LearningItemUpdate
from app.models.models import LearningItem as LearningItemModel

@router.get("/items", response_model=List[LearningItemSchema])
def get_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    topic_id: Optional[int] = None,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    query = db.query(LearningItemModel)
    if topic_id:
        query = query.filter(LearningItemModel.topic_id == topic_id)
    return query.offset(skip).limit(limit).all()

@router.post("/items", response_model=LearningItemSchema)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: LearningItemCreate,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    item = LearningItemModel(**item_in.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/items/{item_id}", response_model=LearningItemSchema)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    item_in: LearningItemUpdate,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    item = db.query(LearningItemModel).filter(LearningItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Bài học không tồn tại")
    
    update_data = item_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
        
    db.commit()
    db.refresh(item)
    return item

@router.delete("/items/{item_id}")
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    item = db.query(LearningItemModel).filter(LearningItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Bài học không tồn tại")
    
    db.delete(item)
    db.commit()
    return {"message": "Đã xóa bài học"}

# ==========================================
# QUIZ MANAGEMENT
# ==========================================
from app.schemas.quiz import Quiz as QuizSchema, QuizCreate, QuizUpdate
from app.models.models import Quiz as QuizModel

@router.get("/quizzes", response_model=List[QuizSchema])
def get_quizzes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    item_id: Optional[int] = None,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    query = db.query(QuizModel)
    if item_id:
        query = query.filter(QuizModel.item_id == item_id)
    return query.offset(skip).limit(limit).all()

@router.post("/quizzes", response_model=QuizSchema)
def create_quiz(
    *,
    db: Session = Depends(deps.get_db),
    quiz_in: QuizCreate,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    quiz = QuizModel(**quiz_in.dict())
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz

@router.put("/quizzes/{quiz_id}", response_model=QuizSchema)
def update_quiz(
    *,
    db: Session = Depends(deps.get_db),
    quiz_id: int,
    quiz_in: QuizUpdate,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    quiz = db.query(QuizModel).filter(QuizModel.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz không tồn tại")
    
    update_data = quiz_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(quiz, field, value)
        
    db.commit()
    db.refresh(quiz)
    return quiz

@router.delete("/quizzes/{quiz_id}")
def delete_quiz(
    *,
    db: Session = Depends(deps.get_db),
    quiz_id: int,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    quiz = db.query(QuizModel).filter(QuizModel.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz không tồn tại")
    
    db.delete(quiz)
    db.commit()
    return {"message": "Đã xóa quiz"}

# --- Questions Management ---
from app.models.models import Question as QuestionModel
from app.schemas.quiz import Question as QuestionSchema, QuestionCreate, QuestionUpdate

@router.get("/quizzes/{quiz_id}/questions", response_model=List[QuestionSchema])
def get_questions_by_quiz(
    quiz_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    questions = db.query(QuestionModel).filter(QuestionModel.quiz_id == quiz_id).order_by(QuestionModel.order_index).all()
    return questions

@router.post("/quizzes/{quiz_id}/questions", response_model=QuestionSchema)
def create_question(
    quiz_id: int,
    question_in: QuestionCreate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    quiz = db.query(QuizModel).filter(QuizModel.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    question_data = question_in.dict()
    question_data["quiz_id"] = quiz_id
    question_data["topic_id"] = quiz.item.topic_id
    
    question = QuestionModel(**question_data)
    db.add(question)
    quiz.total_questions += 1
    db.commit()
    db.refresh(question)
    return question

@router.put("/questions/{question_id}", response_model=QuestionSchema)
def update_question(
    question_id: int,
    question_in: QuestionUpdate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    question = db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    update_data = question_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(question, field, value)
        
    db.commit()
    db.refresh(question)
    return question

@router.delete("/questions/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    question = db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    quiz = db.query(QuizModel).filter(QuizModel.id == question.quiz_id).first()
    if quiz:
        quiz.total_questions = max(0, quiz.total_questions - 1)
        
    db.delete(question)
    db.commit()
    return {"message": "Question deleted successfully"}

# --- Flashcards Management ---
from app.models.models import Flashcard as FlashcardModel
from app.schemas.quiz import Flashcard as FlashcardSchema, FlashcardCreate, FlashcardUpdate

@router.get("/items/{item_id}/flashcards", response_model=List[FlashcardSchema])
def get_flashcards_by_item(
    item_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    flashcards = db.query(FlashcardModel).filter(FlashcardModel.item_id == item_id).order_by(FlashcardModel.order_index).all()
    return flashcards

@router.post("/items/{item_id}/flashcards", response_model=FlashcardSchema)
def create_flashcard(
    item_id: int,
    flashcard_in: FlashcardCreate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    item = db.query(LearningItemModel).filter(LearningItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Learning Item not found")
    
    flashcard_data = flashcard_in.dict()
    flashcard_data["item_id"] = item_id
    
    flashcard = FlashcardModel(**flashcard_data)
    db.add(flashcard)
    db.commit()
    db.refresh(flashcard)
    return flashcard

@router.put("/flashcards/{flashcard_id}", response_model=FlashcardSchema)
def update_flashcard(
    flashcard_id: int,
    flashcard_in: FlashcardUpdate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    flashcard = db.query(FlashcardModel).filter(FlashcardModel.id == flashcard_id).first()
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
        
    update_data = flashcard_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(flashcard, field, value)
        
    db.commit()
    db.refresh(flashcard)
    return flashcard

@router.delete("/flashcards/{flashcard_id}")
def delete_flashcard(
    flashcard_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    flashcard = db.query(FlashcardModel).filter(FlashcardModel.id == flashcard_id).first()
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
        
    db.delete(flashcard)
    db.commit()
    return {"message": "Flashcard deleted successfully"}

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


# --- SURVEY MANAGEMENT ---

from app.models.models import Survey, SurveyQuestion, SurveyOption
from app.schemas.survey import SurveyCreate, SurveyUpdate, SurveyResponse, SurveyQuestionCreate, SurveyQuestionUpdate, SurveyQuestionResponse


@router.get("/surveys/stats/overview")
def get_survey_stats(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
):
    from app.models.models import SurveyAttempt, User
    completed = db.query(SurveyAttempt).filter(SurveyAttempt.status == "completed").count()
    total_users = db.query(User).filter(User.role == "student").count()
    return {"total_completed": completed, "total_users": total_users}

@router.get("/surveys", response_model=List[SurveyResponse])
def get_surveys(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
):
    return db.query(Survey).order_by(Survey.id.desc()).all()

@router.post("/surveys", response_model=SurveyResponse)
def create_survey(
    *,
    db: Session = Depends(deps.get_db),
    survey_in: SurveyCreate,
    current_admin: User = Depends(deps.get_current_active_admin)
):
    survey = Survey(**survey_in.dict())
    db.add(survey)
    db.commit()
    db.refresh(survey)
    return survey

@router.put("/surveys/{survey_id}", response_model=SurveyResponse)
def update_survey(
    *,
    db: Session = Depends(deps.get_db),
    survey_id: int,
    survey_in: SurveyUpdate,
    current_admin: User = Depends(deps.get_current_active_admin)
):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    update_data = survey_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(survey, field, value)
        
    db.commit()
    db.refresh(survey)
    return survey

@router.delete("/surveys/{survey_id}")
def delete_survey(
    *,
    db: Session = Depends(deps.get_db),
    survey_id: int,
    current_admin: User = Depends(deps.get_current_active_admin)
):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    db.delete(survey)
    db.commit()
    return {"ok": True}

@router.post("/surveys/{survey_id}/activate")
def activate_survey(
    *,
    db: Session = Depends(deps.get_db),
    survey_id: int,
    current_admin: User = Depends(deps.get_current_active_admin)
):
    # Deactivate all other surveys
    db.query(Survey).update({"is_active": False})
    
    # Activate the target one
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    survey.is_active = True
    survey.status = "published"
    db.commit()
    return {"ok": True}

# --- SURVEY QUESTIONS ---

@router.get("/surveys/{survey_id}/questions", response_model=List[SurveyQuestionResponse])
def get_survey_questions(
    *,
    db: Session = Depends(deps.get_db),
    survey_id: int,
    current_admin: User = Depends(deps.get_current_active_admin)
):
    return db.query(SurveyQuestion).filter(SurveyQuestion.survey_id == survey_id).order_by(SurveyQuestion.order_index.asc()).all()

@router.post("/surveys/{survey_id}/questions", response_model=SurveyQuestionResponse)
def create_survey_question(
    *,
    db: Session = Depends(deps.get_db),
    survey_id: int,
    question_in: SurveyQuestionCreate,
    current_admin: User = Depends(deps.get_current_active_admin)
):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
        
    question_data = question_in.dict(exclude={"options"})
    question = SurveyQuestion(**question_data, survey_id=survey_id)
    db.add(question)
    db.commit()
    db.refresh(question)
    
    # Add options
    for opt_data in question_in.options:
        opt = SurveyOption(**opt_data.dict(), question_id=question.id)
        db.add(opt)
    
    db.commit()
    db.refresh(question)
    return question

@router.delete("/questions/{question_id}")
def delete_survey_question(
    *,
    db: Session = Depends(deps.get_db),
    question_id: int,
    current_admin: User = Depends(deps.get_current_active_admin)
):
    question = db.query(SurveyQuestion).filter(SurveyQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(question)
    db.commit()
    return {"ok": True}



@router.get("/surveys/active/results")
def get_survey_results(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
):
    from app.models.models import Survey, SurveyAttempt, SurveyAnswer, SurveyQuestion, SurveyOption
    
    survey = db.query(Survey).filter(Survey.is_active == True).first()
    if not survey:
        return []
        
    attempts = db.query(SurveyAttempt).filter(SurveyAttempt.survey_id == survey.id, SurveyAttempt.status == "completed").all()
    
    results = []
    for att in attempts:
        user = db.query(User).filter(User.id == att.user_id).first()
        answers = db.query(SurveyAnswer).filter(SurveyAnswer.attempt_id == att.id).all()
        
        ans_details = []
        for a in answers:
            q = db.query(SurveyQuestion).filter(SurveyQuestion.id == a.question_id).first()
            if not q: continue
            
            val = a.text_value
            if a.option_id:
                opt = db.query(SurveyOption).filter(SurveyOption.id == a.option_id).first()
                if opt:
                    val = opt.content
                    
            ans_details.append({
                "question": q.content,
                "answer": val
            })
            
        results.append({
            "id": att.id,
            "user_name": user.full_name if user else "Unknown",
            "email": user.email if user else "Unknown",
            "completed_at": att.completed_at,
            "total_score": att.total_score,
            "answers": ans_details
        })
        
    return results
