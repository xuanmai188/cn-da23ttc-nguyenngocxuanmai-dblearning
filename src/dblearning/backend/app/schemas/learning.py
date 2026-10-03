from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


# --- Topics ---
class TopicBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = "book"
    color: Optional[str] = "#6366f1"
    order_index: Optional[int] = 0

class Topic(TopicBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class TopicDetail(Topic):
    items: List['LearningItem'] = []

    class Config:
        from_attributes = True


# --- Learning Items ---
class LearningItemBase(BaseModel):
    topic_id: int
    title: str
    description: Optional[str] = None
    content_type: str  # document, video, flashcard_set, quiz
    difficulty: str    # beginner, intermediate, advanced
    content_url: Optional[str] = None
    content_body: Optional[str] = None
    keywords: Optional[List[str]] = None
    estimated_minutes: Optional[int] = 15

class LearningItemCreate(LearningItemBase):
    pass

class LearningItemUpdate(BaseModel):
    topic_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    content_type: Optional[str] = None
    difficulty: Optional[str] = None
    content_url: Optional[str] = None
    content_body: Optional[str] = None
    keywords: Optional[List[str]] = None
    estimated_minutes: Optional[int] = None
    is_active: Optional[bool] = None

class LearningItem(LearningItemBase):
    id: int
    view_count: int
    is_active: bool
    created_at: datetime
    
    # We might include basic topic details when listing items
    topic: Optional[TopicBase] = None

    class Config:
        from_attributes = True


# --- Learning Sessions ---
class LearningSessionCreate(BaseModel):
    item_id: int
    
class LearningSessionUpdate(BaseModel):
    duration_seconds: Optional[int] = None
    completion_rate: Optional[float] = None
    interaction_score: Optional[float] = None
    status: Optional[str] = None  # in_progress, completed, abandoned

class LearningSession(BaseModel):
    id: int
    user_id: int
    item_id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration_seconds: int
    completion_rate: float
    status: str
    
    item: Optional[LearningItemBase] = None

    class Config:
        from_attributes = True


# --- Recommendations ---
class RecommendationBase(BaseModel):
    item_id: int
    score: float
    reason: Optional[str] = None
    rec_type: str

class Recommendation(RecommendationBase):
    id: int
    user_id: int
    is_clicked: bool
    generated_at: datetime
    
    item: Optional[LearningItem] = None

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    recommendations: List[Recommendation]
    generated_at: datetime


# --- Profiles ---
class LearningProfile(BaseModel):
    user_id: int
    topic_scores: Optional[Dict[str, float]] = None
    difficulty_distribution: Optional[Dict[str, float]] = None
    preferred_difficulty: str
    total_study_hours: float
    total_items_completed: int
    total_quizzes_taken: int
    avg_quiz_score: float
    learning_streak: int = 0
    is_onboarded: bool = False
    last_updated: datetime

    class Config:
        from_attributes = True

# --- Onboarding ---
class OnboardingRequest(BaseModel):
    preferred_difficulty: str
    interested_topic_ids: List[int]
