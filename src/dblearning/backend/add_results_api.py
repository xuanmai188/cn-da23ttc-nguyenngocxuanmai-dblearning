file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_endpoint = """
@router.get("/surveys/active/results")
def get_survey_results(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
):
    from app.models.models import Survey, SurveyAttempt, SurveyAnswer, SurveyQuestion, SurveyOption
    
    survey = db.query(Survey).filter(Survey.is_active == True).first()
    if not survey:
        return []
        
    attempts = db.query(SurveyAttempt).filter(SurveyAttempt.survey_id == survey.id, SurveyAttempt.status == "completed").all()
    
    results = []
    for att in attempts:
        user = db.query(User).filter(User.id == att.user_id).first()
        answers = db.query(SurveyAnswer).filter(SurveyAnswer.attempt_id == att.id).all()
        
        ans_details = []
        for a in answers:
            q = db.query(SurveyQuestion).filter(SurveyQuestion.id == a.question_id).first()
            if not q: continue
            
            val = a.text_value
            if a.option_id:
                opt = db.query(SurveyOption).filter(SurveyOption.id == a.option_id).first()
                if opt:
                    val = opt.content
                    
            ans_details.append({
                "question": q.content,
                "answer": val
            })
            
        results.append({
            "id": att.id,
            "user_name": user.full_name if user else "Unknown",
            "email": user.email if user else "Unknown",
            "completed_at": att.completed_at,
            "total_score": att.total_score,
            "answers": ans_details
        })
        
    return results
"""

if "get_survey_results" not in content:
    content = content + "\n" + new_endpoint
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Added survey results endpoint")
