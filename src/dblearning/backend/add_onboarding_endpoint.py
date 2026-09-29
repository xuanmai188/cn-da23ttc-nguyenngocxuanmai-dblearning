file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/recommendation.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import_statement = "from app.schemas.learning import RecommendationResponse, LearningProfile as LearningProfileSchema, OnboardingRequest"
content = content.replace("from app.schemas.learning import RecommendationResponse, LearningProfile as LearningProfileSchema", import_statement)
content = content.replace("from app.models.models import User, Recommendation, LearningProfile", "from app.models.models import User, Recommendation, LearningProfile, Topic")

new_endpoint = """
@router.post("/onboarding", response_model=LearningProfileSchema)
def submit_onboarding(
    request: OnboardingRequest,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    \"\"\"Lưu kết quả khảo sát đầu vào và tạo profile cá nhân hóa ngay lập tức.\"\"\"
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
"""

content = content + new_endpoint

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("recommendation.py endpoint added")
