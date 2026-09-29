import json
from sqlalchemy.orm import Session
from collections import defaultdict
from app.models.models import LearningSession, QuizResult, LearningProfile, Topic, LearningItem
import numpy as np

def update_user_profile(db: Session, user_id: int):
    """
    Xây dựng/cập nhật Learning Profile dựa trên lịch sử học và kết quả kiểm tra.
    """
    # 1. Thu thập dữ liệu
    sessions = db.query(LearningSession).filter(LearningSession.user_id == user_id).all()
    quiz_results = db.query(QuizResult).filter(QuizResult.user_id == user_id).all()

    # Nếu user chưa có lịch sử học nhưng đã làm khảo sát (onboarded), giữ nguyên profile
    profile = db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()
    if profile and profile.is_onboarded and len(sessions) == 0 and len(quiz_results) == 0:
        profile.learning_streak = 0
        db.commit()
        return profile
    
    # Khởi tạo dữ liệu thống kê
    topic_scores = defaultdict(float)
    topic_weights = defaultdict(float)
    difficulty_counts = {"beginner": 0, "intermediate": 0, "advanced": 0}
    total_hours = 0
    total_completed = 0
    
    # 2. Phân tích kết quả Quiz (Trọng số cao)
    for result in quiz_results:
        # Lấy topic của quiz này
        quiz = result.quiz
        if quiz and quiz.item:
            topic_id = str(quiz.item.topic_id)
            # Điểm từ 0-1
            normalized_score = result.score / 100.0
            # Trọng số: Bài kiểm tra có trọng số cao (ví dụ: 0.7)
            topic_scores[topic_id] += normalized_score * 0.7
            topic_weights[topic_id] += 0.7

    # 3. Phân tích Lịch sử Học (Trọng số trung bình)
    # Deduplicate sessions by item_id, keeping the latest one
    unique_sessions = {}
    for session in sessions:
        if session.item_id not in unique_sessions or session.id > unique_sessions[session.item_id].id:
            unique_sessions[session.item_id] = session
            
    for session in unique_sessions.values():
        total_hours += session.duration_seconds / 3600.0
        if session.status == "completed":
            total_completed += 1
            
        item = session.item
        if item:
            topic_id = str(item.topic_id)
            difficulty_counts[item.difficulty] += 1
            
            # Điểm hoàn thành học liệu (trọng số 0.3)
            completion_score = session.completion_rate * 0.3
            topic_scores[topic_id] += completion_score
            topic_weights[topic_id] += 0.3

    # 4. Tính toán Topic Scores cuối cùng
    final_topic_scores = {}
    for t_id, raw_score in topic_scores.items():
        if topic_weights[t_id] > 0:
            final_topic_scores[t_id] = round(raw_score / topic_weights[t_id], 2)
            
    # 5. Xác định Preferred Difficulty
    preferred_diff = "beginner"
    if sum(difficulty_counts.values()) > 0:
        preferred_diff = max(difficulty_counts, key=difficulty_counts.get)
        
    # Tính average quiz score
    avg_score = 0
    if len(quiz_results) > 0:
        avg_score = sum(r.score for r in quiz_results) / len(quiz_results)

    # 6. Xây dựng Profile Vector (để so sánh Cosine Similarity)
    # Lấy danh sách tất cả các topic (sắp xếp theo id)
    all_topics = db.query(Topic).order_by(Topic.id).all()
    profile_vector = []
    
    for t in all_topics:
        tid = str(t.id)
        # Nếu chưa học thì mặc định quan tâm = 0
        score = final_topic_scores.get(tid, 0.0) 
        profile_vector.append(score)

    # 6.5. Tính toán Chuỗi học tập (Learning Streak)
    from datetime import date, timedelta
    
    # Lấy ngày học duy nhất
    study_dates = set()
    for session in sessions:
        if session.started_at:
            study_dates.add(session.started_at.date())
            
    # Sắp xếp ngày giảm dần
    sorted_dates = sorted(list(study_dates), reverse=True)
    
    current_streak = 0
    today = date.today()
    
    if sorted_dates:
        # Check nếu ngày cuối cùng học là hôm nay hoặc hôm qua
        if sorted_dates[0] == today or sorted_dates[0] == today - timedelta(days=1):
            current_streak = 1
            curr_date = sorted_dates[0]
            for i in range(1, len(sorted_dates)):
                if sorted_dates[i] == curr_date - timedelta(days=1):
                    current_streak += 1
                    curr_date = sorted_dates[i]
                else:
                    break
        else:
            current_streak = 0
    else:
        current_streak = 0
        
    # Đảm bảo current_streak >= 1 nếu có session (giống logic cũ)
    if current_streak == 0 and len(sessions) > 0:
        current_streak = 1

    # 7. Cập nhật DB
    profile = db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()
    if not profile:
        profile = LearningProfile(user_id=user_id)
        db.add(profile)
        
    profile.topic_scores = final_topic_scores
    profile.difficulty_distribution = difficulty_counts
    profile.preferred_difficulty = preferred_diff
    profile.profile_vector = profile_vector
    profile.total_study_hours = total_hours
    profile.total_items_completed = total_completed
    profile.total_quizzes_taken = len(quiz_results)
    profile.avg_quiz_score = avg_score
    profile.learning_streak = current_streak
    
    db.commit()
    return profile
