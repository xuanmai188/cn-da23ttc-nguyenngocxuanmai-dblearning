import json
import random
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from app.api import deps
from app.models.models import Quiz, Question, QuizResult, User, Flashcard, FlashcardLog
from app.schemas.quiz import Quiz as QuizSchema, QuizSubmission, QuizResult as QuizResultSchema, QuizResultWithDetails, Flashcard as FlashcardSchema, FlashcardLogCreate

router = APIRouter()

@router.get("/quizzes", response_model=List[QuizSchema])
def get_quizzes(db: Session = Depends(deps.get_db)):
    """Lấy danh sách bài kiểm tra."""
    return db.query(Quiz).all()


@router.get("/item/{item_id}", response_model=QuizSchema)
def get_quiz_by_item(
    item_id: int, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Lấy chi tiết đề thi (đã trộn đáp án và ẩn câu trả lời đúng) qua item_id."""
    quiz = db.query(Quiz).filter(Quiz.item_id == item_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài kiểm tra")
    
    # Shuffle questions if enabled
    questions = quiz.questions
    if quiz.shuffle_questions:
        random.shuffle(questions)
        
    quiz_data = QuizSchema.model_validate(quiz)
    return quiz_data


@router.post("/item/{item_id}/submit", response_model=QuizResultWithDetails)
def submit_quiz_by_item(
    item_id: int,
    submission: QuizSubmission,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    """Chấm điểm bài kiểm tra qua item_id."""
    quiz = db.query(Quiz).filter(Quiz.item_id == item_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài kiểm tra")
        
    correct_count = 0
    total_questions = len(quiz.questions)
    
    # Chấm điểm
    details = []
    for question in quiz.questions:
        if question.id in submission.answers:
            is_correct = (submission.answers[question.id] == question.correct_option)
            if is_correct:
                correct_count += 1
            details.append({
                "question_id": question.id,
                "is_correct": is_correct,
                "correct_option": question.correct_option,
                "explanation": question.explanation
            })
        else:
            details.append({
                "question_id": question.id,
                "is_correct": False,
                "correct_option": question.correct_option,
                "explanation": question.explanation
            })
                
    score = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    is_passed = score >= quiz.pass_score
    
    result = QuizResult(
        user_id=current_user.id,
        quiz_id=quiz.id,
        score=score,
        total_questions=total_questions,
        correct_answers=correct_count,
        answers=submission.answers,
        time_spent_seconds=submission.time_spent_seconds,
        is_passed=is_passed
    )
    
    db.add(result)
    db.commit()
    db.refresh(result)
    
    # Trigger update profile in background here
    
    return {
        "id": result.id,
        "user_id": result.user_id,
        "quiz_id": result.quiz_id,
        "score": result.score,
        "total_questions": result.total_questions,
        "correct_answers": result.correct_answers,
        "answers": result.answers,
        "time_spent_seconds": result.time_spent_seconds,
        "is_passed": result.is_passed,
        "taken_at": result.taken_at,
        "details": details
    }


@router.get("/flashcards/item/{item_id}", response_model=List[FlashcardSchema])
def get_flashcards_by_item(
    item_id: int,
    db: Session = Depends(deps.get_db)
):
    """Lấy danh sách flashcard thuộc về một học liệu (bộ flashcard)."""
    flashcards = db.query(Flashcard).filter(Flashcard.item_id == item_id).all()
    return flashcards


@router.post("/flashcards/log")
def log_flashcard_result(
    log_in: FlashcardLogCreate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    """Ghi nhận kết quả học một thẻ flashcard."""
    log = FlashcardLog(
        user_id=current_user.id,
        flashcard_id=log_in.flashcard_id,
        result=log_in.result,
        response_time_ms=log_in.response_time_ms
    )
    db.add(log)
    db.commit()
    return {"status": "success"}

@router.get("/item/{item_id}/history", response_model=List[QuizResultSchema])
def get_quiz_history_by_item(
    item_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    """Lấy lịch sử làm bài kiểm tra của một học liệu."""
    quiz = db.query(Quiz).filter(Quiz.item_id == item_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài kiểm tra")
    
    results = db.query(QuizResult).filter(
        QuizResult.quiz_id == quiz.id,
        QuizResult.user_id == current_user.id
    ).order_by(desc(QuizResult.taken_at)).all()
    
    return results
