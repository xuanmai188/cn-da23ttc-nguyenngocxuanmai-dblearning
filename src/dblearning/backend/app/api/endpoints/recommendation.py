from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import deps
from app.models.models import User, Recommendation, LearningProfile, Topic
from app.schemas.learning import RecommendationResponse, LearningProfile as LearningProfileSchema, OnboardingRequest
from app.ml.recommender import generate_recommendations
from app.ml.profile_builder import update_user_profile

router = APIRouter()

@router.get("", response_model=RecommendationResponse)
def get_recommendations(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
    force_refresh: bool = False
):
    """
    Lấy danh sách học liệu gợi ý cho người dùng.
    Mặc định lấy từ database cache (bảng recommendations).
    Nếu force_refresh = True, sẽ chạy lại thuật toán ML.
    """
    if force_refresh:
        # Cập nhật profile và sinh gợi ý mới đồng bộ (chờ kết quả)
        update_user_profile(db, current_user.id)
        generate_recommendations(db, current_user.id)
    else:
        # Check xem user có gợi ý chưa, nếu chưa thì tạo ngay
        has_recs = db.query(Recommendation).filter(Recommendation.user_id == current_user.id).first()
        if not has_recs:
            update_user_profile(db, current_user.id)
            generate_recommendations(db, current_user.id)

    recs = db.query(Recommendation).filter(
        Recommendation.user_id == current_user.id
    ).order_by(Recommendation.score.desc()).limit(10).all()
    
    return {
        "recommendations": recs,
        "generated_at": recs[0].generated_at if recs else datetime.utcnow()
    }


@router.get("/profile", response_model=LearningProfileSchema)
def get_learning_profile(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    """Lấy hồ sơ học tập (Learning Profile) của người dùng."""
    # Cập nhật profile để đảm bảo chuỗi học tập (streak) và thống kê luôn chính xác nhất khi load dashboard
    profile = update_user_profile(db, current_user.id)
    return profile

@router.post("/onboarding", response_model=LearningProfileSchema)
def submit_onboarding(
    request: OnboardingRequest,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    """Lưu kết quả khảo sát đầu vào và tạo profile cá nhân hóa ngay lập tức."""
    profile = db.query(LearningProfile).filter(LearningProfile.user_id == current_user.id).first()
    if not profile:
        profile = LearningProfile(user_id=current_user.id)
        db.add(profile)
    
    # 1. Khởi tạo topic_scores với mức điểm 1.0 cho các chủ đề được chọn
    topic_scores = {}
    for tid in request.interested_topic_ids:
        topic_scores[str(tid)] = 1.0
        
    profile.topic_scores = topic_scores
    profile.preferred_difficulty = request.preferred_difficulty
    profile.is_onboarded = True
    profile.learning_streak = 0
    
    # 2. Tạo profile_vector
    all_topics = db.query(Topic).order_by(Topic.id).all()
    profile_vector = []
    for t in all_topics:
        tid = str(t.id)
        profile_vector.append(topic_scores.get(tid, 0.0))
        
    profile.profile_vector = profile_vector
    db.commit()
    db.refresh(profile)
    
    # 3. Kích hoạt thuật toán cập nhật Gợi ý ngay lập tức
    generate_recommendations(db, current_user.id)
    
    return profile
