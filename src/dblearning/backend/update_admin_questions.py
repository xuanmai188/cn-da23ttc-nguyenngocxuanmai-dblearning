file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# We need to import Question, QuestionCreate, QuestionUpdate from app.schemas.quiz
# Let's see if QuestionSchema is imported. In admin.py, it's probably aliased.

# The safest way is to just append the code at the end of admin.py

new_endpoints = """
# --- Questions Management ---
from app.models.models import Question as QuestionModel
from app.schemas.quiz import Question as QuestionSchema, QuestionCreate, QuestionUpdate

@router.get("/quizzes/{quiz_id}/questions", response_model=List[QuestionSchema])
def get_questions_by_quiz(
    quiz_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    questions = db.query(QuestionModel).filter(QuestionModel.quiz_id == quiz_id).order_by(QuestionModel.order_index).all()
    return questions

@router.post("/quizzes/{quiz_id}/questions", response_model=QuestionSchema)
def create_question(
    quiz_id: int,
    question_in: QuestionCreate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    quiz = db.query(QuizModel).filter(QuizModel.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    question_data = question_in.dict()
    question_data["quiz_id"] = quiz_id
    question_data["topic_id"] = quiz.item.topic_id
    
    question = QuestionModel(**question_data)
    db.add(question)
    quiz.total_questions += 1
    db.commit()
    db.refresh(question)
    return question

@router.put("/questions/{question_id}", response_model=QuestionSchema)
def update_question(
    question_id: int,
    question_in: QuestionUpdate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    question = db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    update_data = question_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(question, field, value)
        
    db.commit()
    db.refresh(question)
    return question

@router.delete("/questions/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    question = db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    quiz = db.query(QuizModel).filter(QuizModel.id == question.quiz_id).first()
    if quiz:
        quiz.total_questions = max(0, quiz.total_questions - 1)
        
    db.delete(question)
    db.commit()
    return {"message": "Question deleted successfully"}
"""

content = content + new_endpoints

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Added /questions endpoints to admin.py")
