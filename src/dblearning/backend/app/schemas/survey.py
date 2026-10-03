from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SurveyOptionBase(BaseModel):
    content: str
    value: Optional[str] = None
    is_correct: bool = False
    score: float = 0.0
    order_index: int = 0

class SurveyOptionCreate(SurveyOptionBase):
    pass

class SurveyOptionUpdate(BaseModel):
    content: Optional[str] = None
    value: Optional[str] = None
    is_correct: Optional[bool] = None
    score: Optional[float] = None
    order_index: Optional[int] = None

class SurveyOptionResponse(SurveyOptionBase):
    id: int
    question_id: int

    class Config:
        from_attributes = True

class SurveyQuestionBase(BaseModel):
    content: str
    question_type: str
    category: str
    topic_id: Optional[int] = None
    difficulty: Optional[str] = None
    weight: float = 1.0
    is_required: bool = True
    order_index: int = 0
    status: str = "active"

class SurveyQuestionCreate(SurveyQuestionBase):
    options: List[SurveyOptionCreate] = []

class SurveyQuestionUpdate(BaseModel):
    content: Optional[str] = None
    question_type: Optional[str] = None
    category: Optional[str] = None
    topic_id: Optional[int] = None
    difficulty: Optional[str] = None
    weight: Optional[float] = None
    is_required: Optional[bool] = None
    order_index: Optional[int] = None
    status: Optional[str] = None

class SurveyQuestionResponse(SurveyQuestionBase):
    id: int
    survey_id: int
    created_at: datetime
    updated_at: datetime
    options: List[SurveyOptionResponse] = []

    class Config:
        from_attributes = True

class SurveyBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "draft"
    is_active: bool = False
    version: int = 1
    time_limit_minutes: int = 15

class SurveyCreate(SurveyBase):
    pass

class SurveyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None
    time_limit_minutes: Optional[int] = None

class SurveyResponse(SurveyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    questions: List[SurveyQuestionResponse] = []

    class Config:
        from_attributes = True
