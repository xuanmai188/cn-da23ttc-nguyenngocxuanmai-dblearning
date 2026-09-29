import json
import numpy as np
from sqlalchemy.orm import Session
from sklearn.metrics.pairwise import cosine_similarity
from app.models.models import LearningProfile, LearningItem, Recommendation, Topic, LearningSession

def compute_item_features(db: Session):
    """
    Tính vector đặc trưng cho từng bài học dựa trên chủ đề (One-Hot Encoding).
    Kết hợp với trọng số độ khó để phân biệt bài lý thuyết và bài kiểm tra.
    """
    items = db.query(LearningItem).filter(LearningItem.is_active == True).all()
    all_topics = db.query(Topic).order_by(Topic.id).all()
    topic_ids = [t.id for t in all_topics]
    
    item_matrix = []
    item_mapping = []
    
    for item in items:
        # One-Hot encoding cho Topic
        vector = [1.0 if item.topic_id == tid else 0.0 for tid in topic_ids]
        item_matrix.append(vector)
        item_mapping.append(item)
        
    return np.array(item_matrix), item_mapping

def generate_cold_start_recommendations(db: Session, user_id: int):
    """
    Cold Start Strategy: Dành cho user mới chưa có lịch sử học tập.
    Gợi ý các bài lý thuyết (document) cơ bản theo thứ tự chủ đề,
    ưu tiên cấp độ 'beginner' trước.
    """
    # Lấy tất cả bài document/flashcard_set cơ bản, ưu tiên beginner
    cold_items = db.query(LearningItem).filter(
        LearningItem.is_active == True,
        LearningItem.content_type.in_(['document', 'flashcard_set']),
        LearningItem.difficulty == 'beginner'
    ).order_by(LearningItem.topic_id, LearningItem.id).limit(8).all()

    # Nếu không đủ beginner, lấy thêm intermediate
    if len(cold_items) < 8:
        extra = db.query(LearningItem).filter(
            LearningItem.is_active == True,
            LearningItem.content_type.in_(['document', 'flashcard_set']),
            LearningItem.difficulty == 'intermediate'
        ).order_by(LearningItem.topic_id, LearningItem.id).limit(8 - len(cold_items)).all()
        cold_items += extra

    db.query(Recommendation).filter(Recommendation.user_id == user_id).delete()
    
    recommendations_to_add = []
    for item in cold_items:
        rec = Recommendation(
            user_id=user_id,
            item_id=item.id,
            score=0.0,  # Cold start: chưa có điểm tương đồng
            reason="Gợi ý bắt đầu cho người mới - hãy học lý thuyết cơ bản trước",
            rec_type="cold_start"
        )
        recommendations_to_add.append(rec)
    
    if recommendations_to_add:
        db.bulk_save_objects(recommendations_to_add)
        db.commit()
    
    return recommendations_to_add

def generate_recommendations(db: Session, user_id: int):
    """
    Thuật toán Content-Based Filtering dùng Cosine Similarity.
    
    Xử lý 2 trường hợp:
    - Cold Start: User mới, chưa có lịch sử → Gợi ý bài cơ bản theo thứ tự chương trình
    - Normal: User đã học → Cosine Similarity với profile vector
    """
    # 1. Lấy User Profile
    profile = db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()
    
    # Cold Start: chưa có profile hoặc profile vector toàn 0
    if not profile or not profile.profile_vector:
        return generate_cold_start_recommendations(db, user_id)
    
    user_vector = np.array(profile.profile_vector)
    
    # Kiểm tra nếu vector toàn 0 (user chưa học gì) → Cold Start
    if np.sum(np.abs(user_vector)) < 0.01:
        return generate_cold_start_recommendations(db, user_id)
    
    user_vector = user_vector.reshape(1, -1)
    
    # 2. Lấy Item Features
    item_matrix, item_mapping = compute_item_features(db)
    if len(item_mapping) == 0:
        return []
        
    # 3. Tính độ tương đồng Cosine Similarity
    similarities = cosine_similarity(user_vector, item_matrix)[0]
    
    # 4. Lấy danh sách item đã học để loại trừ
    completed_sessions = db.query(LearningSession).filter(
        LearningSession.user_id == user_id,
        LearningSession.status == 'completed'
    ).all()
    completed_item_ids = {s.item_id for s in completed_sessions}
    
    # 5. Xếp hạng và Gợi ý
    ranked_indices = similarities.argsort()[::-1]  # Giảm dần
    
    # Xóa gợi ý cũ
    db.query(Recommendation).filter(Recommendation.user_id == user_id).delete()
    
    recommendations_to_add = []
    count = 0
    
    for idx in ranked_indices:
        item = item_mapping[idx]
        score = similarities[idx]
        
        # Bỏ qua item đã học hoàn thành
        if item.id in completed_item_ids:
            continue
        
        # Ưu tiên tài liệu và flashcard trước quiz nếu cùng điểm
        # (quiz chỉ nên xuất hiện sau khi user đã học lý thuyết)
        rec = Recommendation(
            user_id=user_id,
            item_id=item.id,
            score=float(score),
            reason="Phù hợp với chủ đề bạn đang quan tâm",
            rec_type="content"
        )
        recommendations_to_add.append(rec)
        count += 1
        
        if count >= 15:
            break
            
    if recommendations_to_add:
        db.bulk_save_objects(recommendations_to_add)
        db.commit()
        
    return recommendations_to_add
