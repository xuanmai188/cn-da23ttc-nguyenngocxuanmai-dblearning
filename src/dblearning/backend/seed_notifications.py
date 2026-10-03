import os
import sys
from datetime import datetime, timedelta

# Add backend dir to python path to import app modules
sys.path.append("D:/DemoCN2026/dblearning/backend")

from app.core.database import SessionLocal, engine
from app.models.models import Base, Notification, User

# Create tables (only creates new ones)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Find admin user
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        print("No admin user found, cannot seed notifications.")
        sys.exit(0)

    # Check if there are already notifications
    existing_count = db.query(Notification).count()
    if existing_count == 0:
        print("Seeding notifications...")
        now = datetime.utcnow()
        notifications = [
            Notification(
                user_id=admin.id,
                title="Học viên mới",
                message="Nguyễn Ngọc Xuân Mai vừa đăng ký tài khoản.",
                type="info",
                is_read=False,
                created_at=now - timedelta(minutes=5)
            ),
            Notification(
                user_id=admin.id,
                title="Hoàn thành bài kiểm tra",
                message="Thiên Trân vừa hoàn thành Bài kiểm tra giữa kỳ với số điểm tuyệt đối 10/10.",
                type="success",
                is_read=False,
                created_at=now - timedelta(hours=2)
            ),
            Notification(
                user_id=admin.id,
                title="Cảnh báo truy cập",
                message="Phát hiện nhiều lần đăng nhập sai mật khẩu từ IP 192.168.1.15.",
                type="warning",
                is_read=False,
                created_at=now - timedelta(days=1)
            ),
            Notification(
                user_id=admin.id,
                title="Hệ thống",
                message="Bản sao lưu cơ sở dữ liệu định kỳ đã được tạo thành công.",
                type="info",
                is_read=True,
                created_at=now - timedelta(days=3)
            )
        ]
        db.bulk_save_objects(notifications)
        db.commit()
        print("Successfully seeded notifications.")
    else:
        print("Notifications already exist, skipping seed.")
finally:
    db.close()
