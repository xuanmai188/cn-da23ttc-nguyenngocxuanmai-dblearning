from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DashboardStats(BaseModel):
    # Card 1
    total_users: int
    total_students: int
    total_admins: int
    user_growth_rate: float
    # Card 2
    total_learning_items: int
    total_topics: int
    item_growth_rate: float
    # Card 3
    total_quizzes: int
    total_questions: int
    quiz_growth_rate: float
    # Card 4
    today_sessions: int
    yesterday_sessions: int
    session_growth_rate: float

class TopicLearningStat(BaseModel):
    name: str
    sessions: int
    color: str

class PerformanceStat(BaseModel):
    completion_rate: float
    avg_quiz_score: float
    quiz_attempt_rate: float
    document_view_rate: float

class ActiveStudent(BaseModel):
    id: int
    full_name: str
    completed_items: int
    quizzes_taken: int
    avg_score: float
    total_hours: float

class PopularLesson(BaseModel):
    id: int
    title: str
    topic_name: str
    view_count: int
    completion_rate: float

class RecentActivity(BaseModel):
    id: int
    user_name: str
    action: str
    target: str
    time_ago: str
    type: str # 'lesson', 'quiz', 'register', 'document', 'flashcard'

class UserStats(BaseModel):
    total: int
    students: int
    admins: int
    blocked: int
    growth_rate: float
    student_rate: float
    admin_rate: float
    blocked_rate: float

class UserItem(BaseModel):
    id: int
    email: str
    full_name: str
    phone_number: Optional[str] = None
    contact_email: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    last_activity_at: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserList(BaseModel):
    users: List[UserItem]
    total: int

class ChartDataPoint(BaseModel):
    date: str
    count: int

class TopicAdminResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    item_count: int
    is_active: bool

    class Config:
        from_attributes = True

class TopicCreateUpdate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    is_active: bool = True

class UserDetailStats(BaseModel):
    completed_lessons: int
    taken_quizzes: int
    avg_score: float
    total_hours: float

class UserDetailResponse(UserItem):
    stats: UserDetailStats
    phone_number: Optional[str] = None

class UserHistoryItem(BaseModel):
    id: int
    action: str
    target: str
    target_type: str
    created_at: datetime
    time_ago: str

class UserHistoryResponse(BaseModel):
    history: List[UserHistoryItem]
