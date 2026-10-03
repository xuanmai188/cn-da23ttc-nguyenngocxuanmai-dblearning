file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_endpoints = """
# --- Flashcards Management ---
from app.models.models import Flashcard as FlashcardModel
from app.schemas.quiz import Flashcard as FlashcardSchema, FlashcardCreate, FlashcardUpdate

@router.get("/items/{item_id}/flashcards", response_model=List[FlashcardSchema])
def get_flashcards_by_item(
    item_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    flashcards = db.query(FlashcardModel).filter(FlashcardModel.item_id == item_id).order_by(FlashcardModel.order_index).all()
    return flashcards

@router.post("/items/{item_id}/flashcards", response_model=FlashcardSchema)
def create_flashcard(
    item_id: int,
    flashcard_in: FlashcardCreate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    item = db.query(LearningItemModel).filter(LearningItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Learning Item not found")
    
    flashcard_data = flashcard_in.dict()
    flashcard_data["item_id"] = item_id
    
    flashcard = FlashcardModel(**flashcard_data)
    db.add(flashcard)
    db.commit()
    db.refresh(flashcard)
    return flashcard

@router.put("/flashcards/{flashcard_id}", response_model=FlashcardSchema)
def update_flashcard(
    flashcard_id: int,
    flashcard_in: FlashcardUpdate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    flashcard = db.query(FlashcardModel).filter(FlashcardModel.id == flashcard_id).first()
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
        
    update_data = flashcard_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(flashcard, field, value)
        
    db.commit()
    db.refresh(flashcard)
    return flashcard

@router.delete("/flashcards/{flashcard_id}")
def delete_flashcard(
    flashcard_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    flashcard = db.query(FlashcardModel).filter(FlashcardModel.id == flashcard_id).first()
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
        
    db.delete(flashcard)
    db.commit()
    return {"message": "Flashcard deleted successfully"}
"""

content = content + new_endpoints

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Added /flashcards endpoints to admin.py")
