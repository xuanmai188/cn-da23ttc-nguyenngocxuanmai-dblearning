file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/student_survey.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_endpoint = """
@router.post("/skip")
def skip_survey(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    from app.models.models import LearningProfile
    profile = db.query(LearningProfile).filter(LearningProfile.user_id == current_user.id).first()
    if not profile:
        profile = LearningProfile(user_id=current_user.id, is_onboarded=True)
        db.add(profile)
    else:
        profile.is_onboarded = True
    db.commit()
    return {"message": "Onboarding skipped"}
"""

if "def skip_survey(" not in content:
    content = content + "\n" + new_endpoint
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Added skip endpoint")
