from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from .learning import TopicBase

# --- Flashcards ---
class FlashcardBase(BaseModel):
    question: str
    answer: str
    hint: Optional[str] = None
    order_index: int = 0

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    hint: Optional[str] = None
    order_index: Optional[int] = None

class Flashcard(FlashcardBase):
    id: int
    item_id: int

    class Config:
        from_attributes = True

class FlashcardLogCreate(BaseModel):
    flashcard_id: int
    result: str # correct, incorrect, skipped
    response_time_ms: Optional[int] = 0

# --- Quizzes ---
class QuestionBase(BaseModel):
    content: str
    options: List[str]
    correct_option: int
    explanation: Optional[str] = None
    difficulty: str = "medium"
    order_index: int = 0

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    content: Optional[str] = None
    options: Optional[List[str]] = None
    correct_option: Optional[int] = None
    explanation: Optional[str] = None
    difficulty: Optional[str] = None
    order_index: Optional[int] = None

class Question(QuestionBase):
    id: int
    quiz_id: int
    topic_id: int
    
    # We shouldn't return correct_option and explanation to the user BEFORE they submit
    class Config:
        from_attributes = True

# Used when returning the quiz to the user to take
class QuestionPublic(BaseModel):
    id: int
    content: str
    options: List[str]
    difficulty: str
    order_index: int

    class Config:
        from_attributes = True

class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    time_limit_minutes: int = 30
    pass_score: int = 60
    total_questions: int = 0

class QuizCreate(QuizBase):
    item_id: int

class QuizUpdate(BaseModel):
    item_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    time_limit_minutes: Optional[int] = None
    pass_score: Optional[int] = None

class Quiz(QuizBase):
    id: int
    item_id: int
    questions: Optional[List[QuestionPublic]] = []

    class Config:
        from_attributes = True

# --- Quiz Submission & Results ---
class QuizSubmission(BaseModel):
    answers: Dict[int, int]  # question_id -> selected_option_index
    time_spent_seconds: int

class QuizResult(BaseModel):
    id: int
    user_id: int
    quiz_id: int
    score: float
    total_questions: int
    correct_answers: int
    answers: Dict[str, Any]
    time_spent_seconds: int
    is_passed: bool
    taken_at: datetime
    
    class Config:
        from_attributes = True


class QuestionResultDetail(BaseModel):
    question_id: int
    is_correct: bool
    correct_option: int
    explanation: Optional[str] = None

class QuizResultWithDetails(QuizResult):
    details: List[QuestionResultDetail]
