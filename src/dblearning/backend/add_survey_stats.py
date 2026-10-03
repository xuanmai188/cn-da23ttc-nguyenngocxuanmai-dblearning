file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_endpoint = """
@router.get("/surveys/stats/overview")
def get_survey_stats(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
):
    from app.models.models import SurveyAttempt
    completed = db.query(SurveyAttempt).filter(SurveyAttempt.status == "completed").count()
    return {"total_completed": completed}
"""

if "get_survey_stats" not in content:
    content = content.replace(
        "@router.get(\"/surveys\", response_model=List[SurveyResponse])",
        new_endpoint + "\n@router.get(\"/surveys\", response_model=List[SurveyResponse])"
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Added survey stats endpoint")
