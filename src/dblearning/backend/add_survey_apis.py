file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"

api_code = """

# --- SURVEY MANAGEMENT ---

from app.models.models import Survey, SurveyQuestion, SurveyOption
from app.schemas.survey import SurveyCreate, SurveyUpdate, SurveyResponse, SurveyQuestionCreate, SurveyQuestionUpdate, SurveyQuestionResponse

@router.get("/surveys", response_model=List[SurveyResponse])
def get_surveys(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
):
    return db.query(Survey).order_by(Survey.id.desc()).all()

@router.post("/surveys", response_model=SurveyResponse)
def create_survey(
    *,
    db: Session = Depends(deps.get_db),
    survey_in: SurveyCreate,
    current_admin: User = Depends(deps.get_current_active_admin)
):
    survey = Survey(**survey_in.dict())
    db.add(survey)
    db.commit()
    db.refresh(survey)
    return survey

@router.put("/surveys/{survey_id}", response_model=SurveyResponse)
def update_survey(
    *,
    db: Session = Depends(deps.get_db),
    survey_id: int,
    survey_in: SurveyUpdate,
    current_admin: User = Depends(deps.get_current_active_admin)
):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    update_data = survey_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(survey, field, value)
        
    db.commit()
    db.refresh(survey)
    return survey

@router.delete("/surveys/{survey_id}")
def delete_survey(
    *,
    db: Session = Depends(deps.get_db),
    survey_id: int,
    current_admin: User = Depends(deps.get_current_active_admin)
):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    db.delete(survey)
    db.commit()
    return {"ok": True}

@router.post("/surveys/{survey_id}/activate")
def activate_survey(
    *,
    db: Session = Depends(deps.get_db),
    survey_id: int,
    current_admin: User = Depends(deps.get_current_active_admin)
):
    # Deactivate all other surveys
    db.query(Survey).update({"is_active": False})
    
    # Activate the target one
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    survey.is_active = True
    survey.status = "published"
    db.commit()
    return {"ok": True}

# --- SURVEY QUESTIONS ---

@router.get("/surveys/{survey_id}/questions", response_model=List[SurveyQuestionResponse])
def get_survey_questions(
    *,
    db: Session = Depends(deps.get_db),
    survey_id: int,
    current_admin: User = Depends(deps.get_current_active_admin)
):
    return db.query(SurveyQuestion).filter(SurveyQuestion.survey_id == survey_id).order_by(SurveyQuestion.order_index.asc()).all()

@router.post("/surveys/{survey_id}/questions", response_model=SurveyQuestionResponse)
def create_survey_question(
    *,
    db: Session = Depends(deps.get_db),
    survey_id: int,
    question_in: SurveyQuestionCreate,
    current_admin: User = Depends(deps.get_current_active_admin)
):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
        
    question_data = question_in.dict(exclude={"options"})
    question = SurveyQuestion(**question_data, survey_id=survey_id)
    db.add(question)
    db.commit()
    db.refresh(question)
    
    # Add options
    for opt_data in question_in.options:
        opt = SurveyOption(**opt_data.dict(), question_id=question.id)
        db.add(opt)
    
    db.commit()
    db.refresh(question)
    return question

@router.delete("/questions/{question_id}")
def delete_survey_question(
    *,
    db: Session = Depends(deps.get_db),
    question_id: int,
    current_admin: User = Depends(deps.get_current_active_admin)
):
    question = db.query(SurveyQuestion).filter(SurveyQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(question)
    db.commit()
    return {"ok": True}

"""

with open(file_path, "a", encoding="utf-8") as f:
    f.write(api_code)
print("Survey endpoints added to admin.py")
