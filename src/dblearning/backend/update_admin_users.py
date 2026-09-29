import os
import re

file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add get_user_stats
new_stats_api = """@router.get("/users/stats")
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

@router.get("/users", response_model=UserList)"""
content = content.replace('@router.get("/users", response_model=UserList)', new_stats_api)

# Replace get_users
old_get_users = """@router.get("/users", response_model=UserList)
def get_users(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    users = db.query(User).order_by(User.id.desc()).all()
    return {
        "users": users,
        "total": len(users)
    }"""
new_get_users = """from typing import Optional

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
    }"""
content = content.replace(old_get_users, new_get_users)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated admin.py with get_user_stats and modified get_users")
