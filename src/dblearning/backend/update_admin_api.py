file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("from app.models.models import User, LearningSession, QuizResult, Topic", "from app.models.models import User, LearningSession, QuizResult, Topic, LearningProfile")

content = content.replace("total_sessions = db.query(LearningSession).count()", """total_sessions = db.query(LearningSession).count()
    total_completed_items = db.query(func.sum(LearningProfile.total_items_completed)).scalar() or 0""")

content = content.replace('"total_sessions": total_sessions,', '"total_sessions": total_sessions,\n        "total_completed_items": int(total_completed_items),')

content = content.replace("""results = db.query(
        func.date(LearningSession.started_at).label('date'),
        func.count(LearningSession.id).label('count')
    ).filter(LearningSession.started_at >= thirty_days_ago).group_by(func.date(LearningSession.started_at)).all()""", """results = db.query(
        func.date(QuizResult.taken_at).label('date'),
        func.count(QuizResult.id).label('count')
    ).filter(QuizResult.taken_at >= thirty_days_ago).group_by(func.date(QuizResult.taken_at)).all()""")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("api/endpoints/admin.py updated")
