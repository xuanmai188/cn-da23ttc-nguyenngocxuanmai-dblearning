file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_apis = """
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
"""

if "def get_notifications(" not in content:
    content += "\n" + new_apis
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Added notification APIs to admin.py")
else:
    print("APIs already exist")
