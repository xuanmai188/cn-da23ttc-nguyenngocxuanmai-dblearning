import re

file_path = "D:/DemoCN2026/dblearning/backend/app/models/models.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add Notification model at the end of the file
notification_model = """
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), default="info") # info, success, warning, error
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="notifications")
"""

if "class Notification(Base):" not in content:
    content += "\n" + notification_model
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Added Notification model")
else:
    print("Notification model already exists")
