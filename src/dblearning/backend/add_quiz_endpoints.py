file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Make sure Quiz schemas are imported
if "QuizCreate" not in content:
    content = content.replace("from app.schemas.quiz import QuizResult, QuizResultWithDetails",
                              "from app.schemas.quiz import QuizResult, QuizResultWithDetails, Quiz, QuizCreate, QuizUpdate")

endpoints = """
# ==========================================
# QUIZ MANAGEMENT
# ==========================================

from app.models.models import Quiz as QuizModel

@router.get("/quizzes", response_model=List[Quiz])
def get_quizzes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    item_id: Optional[int] = None,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    query = db.query(QuizModel)
    if item_id:
        query = query.filter(QuizModel.item_id == item_id)
    return query.offset(skip).limit(limit).all()

@router.post("/quizzes", response_model=Quiz)
def create_quiz(
    *,
    db: Session = Depends(deps.get_db),
    quiz_in: QuizCreate,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    quiz = QuizModel(**quiz_in.dict())
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz

@router.put("/quizzes/{quiz_id}", response_model=Quiz)
def update_quiz(
    *,
    db: Session = Depends(deps.get_db),
    quiz_id: int,
    quiz_in: QuizUpdate,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    quiz = db.query(QuizModel).filter(QuizModel.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz không tồn tại")
    
    update_data = quiz_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(quiz, field, value)
        
    db.commit()
    db.refresh(quiz)
    return quiz

@router.delete("/quizzes/{quiz_id}")
def delete_quiz(
    *,
    db: Session = Depends(deps.get_db),
    quiz_id: int,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    quiz = db.query(QuizModel).filter(QuizModel.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz không tồn tại")
    
    db.delete(quiz)
    db.commit()
    return {"message": "Đã xóa quiz"}
"""

content += endpoints
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Added quiz endpoints to admin.py")
