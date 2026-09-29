file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add imports for new schemas
import_replacement = """from app.schemas.admin import (
    DashboardStats, UserList, UserItem, ChartDataPoint, TopicAdminResponse, TopicCreateUpdate,
    TopicLearningStat, PerformanceStat, ActiveStudent, PopularLesson, RecentActivity,
    UserStats, UserDetailResponse, UserHistoryResponse
)"""
content = content.replace(
    "from app.schemas.admin import (\n    DashboardStats, UserList, UserItem, ChartDataPoint, TopicAdminResponse, TopicCreateUpdate,\n    TopicLearningStat, PerformanceStat, ActiveStudent, PopularLesson, RecentActivity\n)",
    import_replacement
)


new_endpoints = """@router.get("/users/{user_id}/details", response_model=UserDetailResponse)
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
    ).join(LearningItem, LearningSession.item_id == LearningItem.id) \\
     .filter(LearningSession.user_id == user_id) \\
     .order_by(desc(LearningSession.started_at)) \\
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
"""

content = content + "\n" + new_endpoints

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated admin.py with user detail and history endpoints")
