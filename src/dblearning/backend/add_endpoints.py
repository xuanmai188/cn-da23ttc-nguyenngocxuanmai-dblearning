file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Make sure LearningItem is imported
if "LearningItemCreate" not in content:
    content = content.replace("from app.schemas.learning import Topic, TopicCreate, TopicUpdate, TopicDetail",
                              "from app.schemas.learning import Topic, TopicCreate, TopicUpdate, TopicDetail, LearningItem, LearningItemCreate, LearningItemUpdate")

# Add endpoints
endpoints = """
# ==========================================
# LESSONS (ITEMS) MANAGEMENT
# ==========================================

from app.models.models import LearningItem as LearningItemModel

@router.get("/items", response_model=List[LearningItem])
def get_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    topic_id: Optional[int] = None,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    query = db.query(LearningItemModel)
    if topic_id:
        query = query.filter(LearningItemModel.topic_id == topic_id)
    return query.offset(skip).limit(limit).all()

@router.post("/items", response_model=LearningItem)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: LearningItemCreate,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    item = LearningItemModel(**item_in.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.put("/items/{item_id}", response_model=LearningItem)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    item_in: LearningItemUpdate,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    item = db.query(LearningItemModel).filter(LearningItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Bài học không tồn tại")
    
    update_data = item_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
        
    db.commit()
    db.refresh(item)
    return item

@router.delete("/items/{item_id}")
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    item = db.query(LearningItemModel).filter(LearningItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Bài học không tồn tại")
    
    db.delete(item)
    db.commit()
    return {"message": "Đã xóa bài học"}
"""
content += endpoints
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Added endpoints to admin.py")
