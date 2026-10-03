file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_endpoint = """
@router.get("/surveys/stats/overview")
def get_survey_stats(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
):
    from app.models.models import SurveyAttempt, User
    completed = db.query(SurveyAttempt).filter(SurveyAttempt.status == "completed").count()
    total_users = db.query(User).filter(User.role == "student").count()
    return {"total_completed": completed, "total_users": total_users}
"""

import re
content = re.sub(r'@router.get\("/surveys/stats/overview"\).*?return {"total_completed": completed}', new_endpoint.strip(), content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated survey stats endpoint to include total_users")
