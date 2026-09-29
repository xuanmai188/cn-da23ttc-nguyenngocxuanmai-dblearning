file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
content = """from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any
from sqlalchemy import func

from app.api import deps
from app.models.models import User, LearningSession, QuizResult
from app.schemas.admin import DashboardStats, UserList, UserItem

router = APIRouter()

@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_sessions = db.query(LearningSession).count()
    total_quizzes = db.query(QuizResult).count()
    
    # Calc avg completion rate
    sessions = db.query(LearningSession.completion_rate).all()
    avg_rate = sum(s[0] for s in sessions) / len(sessions) if sessions else 0.0
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_sessions": total_sessions,
        "total_quizzes": total_quizzes,
        "avg_completion_rate": round(avg_rate * 100, 2)
    }

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
"""
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Admin endpoints written")
