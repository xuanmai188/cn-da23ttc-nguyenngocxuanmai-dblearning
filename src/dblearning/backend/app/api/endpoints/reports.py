from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_, and_
from typing import Optional, List, Dict
from datetime import datetime
import json

from app.api import deps
from app.models.models import (
    User, LearningSession, LearningItem, Topic, QuizResult, Quiz,
    Recommendation, Survey, SurveyAttempt, SurveyAnswer, SurveyQuestion, SurveyOption
)

router = APIRouter()

def apply_filters(query, model, date_column, start_date: Optional[str], end_date: Optional[str]):
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00")).replace(tzinfo=None)
            query = query.filter(date_column >= start_dt)
        except Exception:
            pass
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00")).replace(tzinfo=None)
            query = query.filter(date_column <= end_dt)
        except Exception:
            pass
    return query

@router.get("/learning-activity")
def get_learning_activity(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    topic_id: Optional[int] = None,
    item_type: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
):
    # Base query for sessions
    q = db.query(LearningSession).join(LearningItem, LearningSession.item_id == LearningItem.id)
    q = apply_filters(q, LearningSession, LearningSession.started_at, start_date, end_date)
    
    if topic_id:
        q = q.filter(LearningItem.topic_id == topic_id)
    if item_type:
        q = q.filter(LearningItem.content_type == item_type)
        
    sessions = q.all()
    
    total_views = len(sessions)
    total_completed = len([s for s in sessions if s.status == "completed"])
    completion_rate = round((total_completed / total_views * 100) if total_views > 0 else 0, 2)
    
    # Detail Table
    details_dict = {}
    for s in sessions:
        item = db.query(LearningItem).filter(LearningItem.id == s.item_id).first()
        topic = db.query(Topic).filter(Topic.id == item.topic_id).first() if item.topic_id else None
        key = item.id
        if key not in details_dict:
            details_dict[key] = {
                "id": item.id,
                "title": item.title,
                "topic": topic.name if topic else "Chung",
                "type": item.content_type,
                "views": 0,
                "completed": 0
            }
        details_dict[key]["views"] += 1
        if s.status == "completed":
            details_dict[key]["completed"] += 1
            
    details_list = list(details_dict.values())
    for d in details_list:
        d["completion_rate"] = round((d["completed"] / d["views"] * 100) if d["views"] > 0 else 0, 2)
        
    details_list.sort(key=lambda x: x["views"], reverse=True)
    
    # Activity Distribution
    distribution = {
        "lesson": len([d for d in details_list if d["type"] == "lesson"]),
        "document": len([d for d in details_list if d["type"] == "document"]),
        "quiz": len([d for d in details_list if d["type"] == "quiz"]),
        "flashcard": len([d for d in details_list if d["type"] == "flashcard"])
    }
    
    return {
        "summary": {
            "total_views": total_views,
            "total_completed": total_completed,
            "completion_rate": completion_rate,
            "distribution": distribution
        },
        "details": details_list
    }

@router.get("/learning-results")
def get_learning_results(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    topic_id: Optional[int] = None,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
):
    q = db.query(QuizResult).join(Quiz, QuizResult.quiz_id == Quiz.id).join(LearningItem, Quiz.item_id == LearningItem.id)
    q = apply_filters(q, QuizResult, QuizResult.taken_at, start_date, end_date)
    
    if topic_id:
        q = q.filter(LearningItem.topic_id == topic_id)
        
    results = q.all()
    
    total_attempts = len(results)
    avg_score = round(sum([r.score for r in results]) / total_attempts if total_attempts > 0 else 0, 2)
    total_passed = len([r for r in results if r.is_passed])
    pass_rate = round((total_passed / total_attempts * 100) if total_attempts > 0 else 0, 2)
    
    # Detail Table
    details_dict = {}
    for r in results:
        quiz = db.query(Quiz).filter(Quiz.id == r.quiz_id).first()
        item = db.query(LearningItem).filter(LearningItem.id == quiz.item_id).first()
        topic = db.query(Topic).filter(Topic.id == item.topic_id).first() if item.topic_id else None
        topic_name = topic.name if topic else "Chung"
        
        if topic_name not in details_dict:
            details_dict[topic_name] = {
                "topic": topic_name,
                "attempts": 0,
                "total_score": 0,
                "passed": 0,
                "unique_students": set()
            }
        details_dict[topic_name]["attempts"] += 1
        details_dict[topic_name]["total_score"] += r.score
        if r.is_passed:
            details_dict[topic_name]["passed"] += 1
        details_dict[topic_name]["unique_students"].add(r.user_id)
        
    details_list = []
    for t_name, d in details_dict.items():
        details_list.append({
            "topic": t_name,
            "students_count": len(d["unique_students"]),
            "attempts": d["attempts"],
            "avg_score": round(d["total_score"] / d["attempts"], 2) if d["attempts"] > 0 else 0,
            "pass_rate": round(d["passed"] / d["attempts"] * 100, 2) if d["attempts"] > 0 else 0
        })
        
    details_list.sort(key=lambda x: x["attempts"], reverse=True)
    
    return {
        "summary": {
            "avg_score": avg_score,
            "total_attempts": total_attempts,
            "pass_rate": pass_rate,
            "total_students": len(set([r.user_id for r in results]))
        },
        "details": details_list
    }

@router.get("/recommendations")
def get_recommendation_reports(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
):
    q = db.query(Recommendation)
    q = apply_filters(q, Recommendation, Recommendation.generated_at, start_date, end_date)
    
    recs = q.all()
    
    total_recs = len(recs)
    clicked_recs = len([r for r in recs if r.is_clicked])
    click_rate = round((clicked_recs / total_recs * 100) if total_recs > 0 else 0, 2)
    avg_score = round(sum([r.score for r in recs]) / total_recs if total_recs > 0 else 0, 2)
    
    # Detail Table (Limit to 100 to prevent huge payload, or we could paginate)
    details_list = []
    for r in sorted(recs, key=lambda x: x.generated_at, reverse=True)[:100]:
        user = db.query(User).filter(User.id == r.user_id).first()
        item = db.query(LearningItem).filter(LearningItem.id == r.item_id).first()
        topic = db.query(Topic).filter(Topic.id == item.topic_id).first() if item and item.topic_id else None
        
        details_list.append({
            "id": r.id,
            "user_name": user.full_name if user else "Unknown",
            "item_title": item.title if item else "Unknown",
            "item_type": item.content_type if item else "Unknown",
            "topic": topic.name if topic else "Chung",
            "score": round(r.score, 2),
            "is_clicked": r.is_clicked,
            "generated_at": r.generated_at
        })
        
    # Distribution
    dist = {}
    for d in details_list:
        dist[d["item_type"]] = dist.get(d["item_type"], 0) + 1
        
    return {
        "summary": {
            "total_recs": total_recs,
            "total_students": len(set([r.user_id for r in recs])),
            "clicked_recs": clicked_recs,
            "click_rate": click_rate,
            "avg_score": avg_score,
            "distribution": dist
        },
        "details": details_list
    }

@router.get("/surveys")
def get_survey_reports(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
):
    # Re-use logic from admin.py /surveys/active/results, but aggregate
    survey = db.query(Survey).filter(Survey.is_active == True).first()
    if not survey:
        survey = db.query(Survey).order_by(Survey.id.desc()).first()
        
    if not survey:
        return {"summary": {}, "details": []}
        
    q = db.query(SurveyAttempt).filter(SurveyAttempt.survey_id == survey.id, SurveyAttempt.status == "completed")
    q = apply_filters(q, SurveyAttempt, SurveyAttempt.completed_at, start_date, end_date)
    
    attempts = q.all()
    total_users = db.query(User).filter(User.role == "student").count()
    completed = len(attempts)
    completion_rate = round((completed / total_users * 100) if total_users > 0 else 0, 2)
    
    details_list = []
    
    for att in attempts:
        user = db.query(User).filter(User.id == att.user_id).first()
        answers = db.query(SurveyAnswer).filter(SurveyAnswer.attempt_id == att.id).all()
        
        interest = []
        goal = []
        knowledge_score = att.total_score or 0
        
        for a in answers:
            q = db.query(SurveyQuestion).filter(SurveyQuestion.id == a.question_id).first()
            if not q: continue
            
            val = a.text_value
            if a.option_id:
                opt = db.query(SurveyOption).filter(SurveyOption.id == a.option_id).first()
                if opt:
                    val = opt.content
                    
            if q.category == "interest":
                interest.append(val)
            elif q.category == "goal":
                goal.append(val)
                
        details_list.append({
            "id": att.id,
            "user_id": user.id if user else None,
            "user_name": user.full_name if user else "Unknown",
            "knowledge_score": knowledge_score,
            "interests": ", ".join(interest) if interest else "Không có",
            "goals": ", ".join(goal) if goal else "Không có",
            "completed_at": att.completed_at
        })
        
    return {
        "summary": {
            "total_users": total_users,
            "completed": completed,
            "pending": total_users - completed,
            "completion_rate": completion_rate
        },
        "details": details_list
    }
