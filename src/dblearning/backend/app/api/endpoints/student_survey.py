from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime

from app.api import deps
from app.models.models import User, Survey, SurveyQuestion, SurveyOption, SurveyAttempt, SurveyAnswer, LearningProfile, Topic
from pydantic import BaseModel
from app.ml.recommender import generate_recommendations

router = APIRouter()

class AnswerItem(BaseModel):
    question_id: int
    option_ids: List[int] = []
    text_value: str = None

class SurveySubmitRequest(BaseModel):
    answers: List[AnswerItem]

@router.get("/active")
def get_active_survey(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    survey = db.query(Survey).filter(Survey.is_active == True).first()
    if not survey:
        raise HTTPException(status_code=404, detail="No active survey found")
    
    questions = db.query(SurveyQuestion).filter(SurveyQuestion.survey_id == survey.id).order_by(SurveyQuestion.order_index).all()
    
    q_list = []
    for q in questions:
        options = db.query(SurveyOption).filter(SurveyOption.question_id == q.id).order_by(SurveyOption.order_index).all()
        q_list.append({
            "id": q.id,
            "content": q.content,
            "question_type": q.question_type,
            "category": q.category,
            "difficulty": q.difficulty,
            "is_required": q.is_required,
            "options": [{"id": o.id, "content": o.content, "value": o.value} for o in options]
        })
        
    return {
        "id": survey.id,
        "title": survey.title,
        "description": survey.description,
        "questions": q_list
    }

@router.post("/{survey_id}/submit")
def submit_survey(
    survey_id: int,
    request: SurveySubmitRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
        
    attempt = db.query(SurveyAttempt).filter(
        SurveyAttempt.survey_id == survey_id,
        SurveyAttempt.user_id == current_user.id
    ).first()
    
    if not attempt:
        attempt = SurveyAttempt(
            survey_id=survey_id,
            user_id=current_user.id,
            status="completed",
            completed_at=datetime.utcnow()
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
    else:
        # Clear old answers
        db.query(SurveyAnswer).filter(SurveyAnswer.attempt_id == attempt.id).delete()
        attempt.completed_at = datetime.utcnow()
        attempt.status = "completed"
    
    total_score = 0
    interested_topic_ids = []
    preferred_difficulty = "beginner"
    
    for ans in request.answers:
        q = db.query(SurveyQuestion).filter(SurveyQuestion.id == ans.question_id).first()
        if not q: continue
        
        for opt_id in ans.option_ids:
            opt = db.query(SurveyOption).filter(SurveyOption.id == opt_id).first()
            if opt:
                score = opt.score * q.weight
                total_score += score
                db.add(SurveyAnswer(
                    attempt_id=attempt.id,
                    question_id=q.id,
                    option_id=opt.id,
                    score=score
                ))
                
                # Analyze for profile
                if q.category == 'interest' and q.topic_id:
                    interested_topic_ids.append(q.topic_id)
                if q.category == 'self_assessment':
                    if opt.value in ["beginner", "intermediate", "advanced"]:
                        preferred_difficulty = opt.value
                        
        if ans.text_value:
            db.add(SurveyAnswer(
                attempt_id=attempt.id,
                question_id=q.id,
                text_value=ans.text_value,
                score=0
            ))
            
    attempt.total_score = total_score
    db.commit()
    
    # UPDATE LEARNING PROFILE
    profile = db.query(LearningProfile).filter(LearningProfile.user_id == current_user.id).first()
    if not profile:
        profile = LearningProfile(user_id=current_user.id)
        db.add(profile)
        
    topic_scores = profile.topic_scores or {}
    for tid in interested_topic_ids:
        topic_scores[str(tid)] = 1.0
        
    profile.topic_scores = topic_scores
    profile.preferred_difficulty = preferred_difficulty
    profile.is_onboarded = True
    
    all_topics = db.query(Topic).order_by(Topic.id).all()
    profile_vector = []
    for t in all_topics:
        profile_vector.append(topic_scores.get(str(t.id), 0.0))
    profile.profile_vector = profile_vector
    
    db.commit()
    generate_recommendations(db, current_user.id)
    
    return {"ok": True, "total_score": total_score}


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
