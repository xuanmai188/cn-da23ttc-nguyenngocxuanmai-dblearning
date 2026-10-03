from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.models import Survey, SurveyQuestion, SurveyOption, Topic
import json

db = SessionLocal()

# Delete existing
db.query(Survey).delete()
db.commit()

# 1. Create Survey
survey = Survey(
    title="Khảo sát Đầu vào Môn Cơ sở dữ liệu",
    description="Vui lòng hoàn thành khảo sát này để hệ thống thiết lập lộ trình học tập tối ưu nhất cho bạn.",
    status="published",
    is_active=True,
    time_limit_minutes=10
)
db.add(survey)
db.commit()
db.refresh(survey)

topics = {t.name: t.id for t in db.query(Topic).all()}
def get_topic(name):
    for k, v in topics.items():
        if name.lower() in k.lower():
            return v
    return None

sql_topic = get_topic("sql")
erd_topic = get_topic("thực thể") or get_topic("er")

# 2. Q1: Kiến thức SQL (self_assessment)
q1 = SurveyQuestion(
    survey_id=survey.id,
    content="Bạn đánh giá kiến thức SQL của mình ở mức nào?",
    question_type="single_choice",
    category="self_assessment",
    difficulty="beginner",
    is_required=True,
    order_index=0
)
db.add(q1)
db.commit()
db.refresh(q1)
db.add_all([
    SurveyOption(question_id=q1.id, content="Chưa biết gì", value="beginner", order_index=0),
    SurveyOption(question_id=q1.id, content="Đã biết cơ bản (Select, Insert...)", value="intermediate", order_index=1),
    SurveyOption(question_id=q1.id, content="Thành thạo (Join, Subquery...)", value="advanced", order_index=2)
])

# 3. Q2: ERD (knowledge/self_assessment)
q2 = SurveyQuestion(
    survey_id=survey.id,
    content="Bạn đã từng thiết kế mô hình Thực thể - Liên kết (ERD) chưa?",
    question_type="single_choice",
    category="knowledge",
    topic_id=erd_topic,
    difficulty="beginner",
    is_required=True,
    order_index=1
)
db.add(q2)
db.commit()
db.refresh(q2)
db.add_all([
    SurveyOption(question_id=q2.id, content="Chưa từng nghe qua", score=0, order_index=0),
    SurveyOption(question_id=q2.id, content="Biết sơ qua nhưng chưa vẽ bao giờ", score=1, order_index=1),
    SurveyOption(question_id=q2.id, content="Đã từng thiết kế ERD thực tế", score=2, is_correct=True, order_index=2)
])

# 4. Q3: Khóa chính/Khóa ngoại (knowledge)
q3 = SurveyQuestion(
    survey_id=survey.id,
    content="Khóa chính (Primary Key) có đặc điểm nào sau đây?",
    question_type="single_choice",
    category="knowledge",
    difficulty="intermediate",
    is_required=True,
    order_index=2
)
db.add(q3)
db.commit()
db.refresh(q3)
db.add_all([
    SurveyOption(question_id=q3.id, content="Định danh duy nhất một dòng trong bảng", score=1, is_correct=True, order_index=0),
    SurveyOption(question_id=q3.id, content="Liên kết với bảng khác", score=0, order_index=1),
    SurveyOption(question_id=q3.id, content="Có thể chứa giá trị NULL", score=0, order_index=2)
])

# 5. Q4: Nhu cầu học tập (interest)
q4 = SurveyQuestion(
    survey_id=survey.id,
    content="Nội dung nào bạn muốn tập trung cải thiện nhất?",
    question_type="multiple_choice",
    category="interest",
    is_required=True,
    order_index=3
)
db.add(q4)
db.commit()
db.refresh(q4)
db.add_all([
    SurveyOption(question_id=q4.id, content="Viết truy vấn SQL", value="sql", order_index=0),
    SurveyOption(question_id=q4.id, content="Thiết kế CSDL (ERD, Chuẩn hóa)", value="design", order_index=1),
    SurveyOption(question_id=q4.id, content="Tối ưu hiệu suất, Index, Transaction", value="performance", order_index=2)
])

# 6. Q5: Mục tiêu (goal)
q5 = SurveyQuestion(
    survey_id=survey.id,
    content="Mục tiêu học tập chính của bạn là gì?",
    question_type="text",
    category="goal",
    is_required=False,
    order_index=4
)
db.add(q5)

db.commit()
print("Seeded survey data successfully!")
