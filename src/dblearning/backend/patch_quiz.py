import os

schema_path = "D:/DemoCN2026/dblearning/backend/app/schemas/quiz.py"
with open(schema_path, "r", encoding="utf-8") as f:
    content = f.read()

if "class QuestionResultDetail" not in content:
    content += """

class QuestionResultDetail(BaseModel):
    question_id: int
    is_correct: bool
    correct_option: int
    explanation: Optional[str] = None

class QuizResultWithDetails(QuizResult):
    details: List[QuestionResultDetail]
"""
    with open(schema_path, "w", encoding="utf-8") as f:
        f.write(content)


endpoint_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/quiz.py"
with open(endpoint_path, "r", encoding="utf-8") as f:
    content = f.read()

if "QuizResultWithDetails" not in content:
    content = content.replace("from app.schemas.quiz import Quiz as QuizSchema, QuizSubmission, QuizResult as QuizResultSchema", "from app.schemas.quiz import Quiz as QuizSchema, QuizSubmission, QuizResult as QuizResultSchema, QuizResultWithDetails")
    
    # Replace the return type of the route
    content = content.replace("@router.post(\"/item/{item_id}/submit\", response_model=QuizResultSchema)", "@router.post(\"/item/{item_id}/submit\", response_model=QuizResultWithDetails)")
    
    # Find the loop and add details
    old_loop = """    # Chấm điểm
    for question in quiz.questions:
        # Nếu user có chọn đáp án cho câu này
        if question.id in submission.answers:
            if submission.answers[question.id] == question.correct_option:
                correct_count += 1"""
                
    new_loop = """    # Chấm điểm
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
            })"""
    content = content.replace(old_loop, new_loop)
    
    old_return = """    db.add(result)
    db.commit()
    db.refresh(result)
    
    # Trigger update profile in background here
    
    return result"""
    
    new_return = """    db.add(result)
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
    }"""
    content = content.replace(old_return, new_return)
    
    with open(endpoint_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Backend Quiz API patched")
