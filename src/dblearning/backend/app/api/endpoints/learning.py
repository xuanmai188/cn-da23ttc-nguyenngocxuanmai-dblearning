from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.api import deps
from app.models.models import Topic, LearningItem, LearningSession, User, Recommendation, Quiz, QuizResult
from app.ml.profile_builder import update_user_profile
from app.schemas.learning import Topic as TopicSchema, TopicDetail as TopicDetailSchema, LearningItem as LearningItemSchema, LearningSession as LearningSessionSchema, LearningSessionCreate, LearningSessionUpdate


def run_profile_update(user_id: int):
    db = next(deps.get_db())
    try:
        update_user_profile(db, user_id)
    finally:
        db.close()

router = APIRouter()

@router.get("/topics", response_model=List[TopicSchema])
def get_topics(db: Session = Depends(deps.get_db)):
    """Lấy danh sách các chủ đề."""
    return db.query(Topic).filter(Topic.is_active == True).order_by(Topic.order_index).all()


@router.get("/topics/{topic_id}", response_model=TopicDetailSchema)
def get_topic_detail(topic_id: int, db: Session = Depends(deps.get_db)):
    """Lấy chi tiết 1 chủ đề kèm danh sách bài học."""
    topic = db.query(Topic).filter(Topic.id == topic_id, Topic.is_active == True).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Không tìm thấy chủ đề")
    
    # Lấy danh sách learning items của topic này
    items = db.query(LearningItem).filter(
        LearningItem.topic_id == topic_id, 
        LearningItem.is_active == True
    ).order_by(LearningItem.id).all()
    
    # Trả về kèm items
    setattr(topic, 'items', items)
    return topic

@router.get("/items", response_model=List[LearningItemSchema])
def get_learning_items(
    topic_id: Optional[int] = None,
    content_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(deps.get_db)
):
    """Lấy danh sách học liệu có lọc."""
    query = db.query(LearningItem).filter(LearningItem.is_active == True)
    
    if topic_id:
        query = query.filter(LearningItem.topic_id == topic_id)
    if content_type:
        query = query.filter(LearningItem.content_type == content_type)
    if difficulty:
        query = query.filter(LearningItem.difficulty == difficulty)
        
    return query.all()


@router.get("/items/{item_id}", response_model=LearningItemSchema)
def get_learning_item(
    item_id: int, 
    db: Session = Depends(deps.get_db)
):
    """Lấy chi tiết 1 học liệu."""
    item = db.query(LearningItem).filter(LearningItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy học liệu")
    
    # Tăng view_count
    item.view_count += 1
    db.commit()
    
    return item


@router.post("/sessions", response_model=LearningSessionSchema)
def start_learning_session(
    session_in: LearningSessionCreate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    """Bắt đầu một phiên học mới (Mở tài liệu/video)."""
    item = db.query(LearningItem).filter(LearningItem.id == session_in.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy học liệu")

    # Nếu đã có session in_progress thì trả lại ngay (tránh tạo nhiều session)
    existing_inprogress = db.query(LearningSession).filter(
        LearningSession.user_id == current_user.id,
        LearningSession.item_id == session_in.item_id,
        LearningSession.status == "in_progress"
    ).first()

    if existing_inprogress:
        return existing_inprogress

    # Nếu đã có session completed, trả về session đó (không tạo mới)
    existing_completed = db.query(LearningSession).filter(
        LearningSession.user_id == current_user.id,
        LearningSession.item_id == session_in.item_id,
        LearningSession.status == "completed"
    ).order_by(LearningSession.id.desc()).first()

    if existing_completed:
        return existing_completed

    session = LearningSession(
        user_id=current_user.id,
        item_id=session_in.item_id,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.put("/sessions/{session_id}", response_model=LearningSessionSchema)
def update_learning_session(
    session_id: int,
    session_in: LearningSessionUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    """Cập nhật tiến độ học tập (Hoàn thành tài liệu, thời gian học)."""
    session = db.query(LearningSession).filter(
        LearningSession.id == session_id,
        LearningSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên học")

    if session_in.duration_seconds is not None:
        session.duration_seconds = session_in.duration_seconds
    if session_in.completion_rate is not None:
        session.completion_rate = session_in.completion_rate
    if session_in.interaction_score is not None:
        session.interaction_score = session_in.interaction_score
    if session_in.status is not None:
        session.status = session_in.status
        if session_in.status == "completed":
            from datetime import datetime
            session.ended_at = datetime.utcnow()
            
            # Đánh dấu đã click nếu học liệu này nằm trong danh sách gợi ý
            rec = db.query(Recommendation).filter(
                Recommendation.user_id == current_user.id,
                Recommendation.item_id == session.item_id,
                Recommendation.is_clicked == False
            ).first()
            if rec:
                rec.is_clicked = True
                rec.clicked_at = datetime.utcnow()

    db.commit()
    db.refresh(session)
    
    # Cập nhật profile sau khi hoàn thành
    background_tasks.add_task(run_profile_update, user_id=current_user.id)
    
    return session

@router.get("/completed-items", response_model=List[int])
def get_completed_items(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    """Lấy danh sách ID các bài học đã hoàn thành của user hiện tại."""
    completed_sessions = db.query(LearningSession.item_id).filter(
        LearningSession.user_id == current_user.id,
        LearningSession.status == "completed"
    ).all()
    
    # Also add quizzes passed if they are considered "completed" (or maybe session covers it? 
    # Usually quiz creates a session too, but let's check QuizResult to be sure)
    passed_quizzes = db.query(Quiz.item_id).join(QuizResult).filter(
        QuizResult.user_id == current_user.id,
        QuizResult.is_passed == True
    ).all()
    
    item_ids = set([item[0] for item in completed_sessions])
    item_ids.update([item[0] for item in passed_quizzes])
    
    return list(item_ids)
