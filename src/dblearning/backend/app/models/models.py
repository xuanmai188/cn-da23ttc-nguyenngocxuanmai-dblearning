from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    contact_email = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    role = Column(Enum("student", "admin"), default="student")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    sessions = relationship("LearningSession", back_populates="user")
    quiz_results = relationship("QuizResult", back_populates="user")
    flashcard_logs = relationship("FlashcardLog", back_populates="user")
    profile = relationship("LearningProfile", back_populates="user", uselist=False)
    recommendations = relationship("Recommendation", back_populates="user")
    learning_paths = relationship("LearningPath", back_populates="user")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(100), default="book")
    color = Column(String(20), default="#6366f1")
    order_index = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    learning_items = relationship("LearningItem", back_populates="topic")
    questions = relationship("Question", back_populates="topic")


class LearningItem(Base):
    __tablename__ = "learning_items"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    content_type = Column(Enum("document", "video", "flashcard_set", "quiz"), nullable=False)
    difficulty = Column(Enum("beginner", "intermediate", "advanced"), default="beginner")
    content_url = Column(String(1000), nullable=True)
    keywords = Column(JSON, nullable=True)
    tfidf_vector = Column(JSON, nullable=True)
    content_body = Column(Text, nullable=True)
    estimated_minutes = Column(Integer, default=15)
    view_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    topic = relationship("Topic", back_populates="learning_items")
    flashcards = relationship("Flashcard", back_populates="item")
    quiz = relationship("Quiz", back_populates="item", uselist=False)
    sessions = relationship("LearningSession", back_populates="item")
    recommendations = relationship("Recommendation", back_populates="item")


class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("learning_items.id", ondelete="CASCADE"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    hint = Column(String(500), nullable=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    item = relationship("LearningItem", back_populates="flashcards")
    logs = relationship("FlashcardLog", back_populates="flashcard")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("learning_items.id", ondelete="CASCADE"), unique=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    time_limit_minutes = Column(Integer, default=30)
    pass_score = Column(Integer, default=60)
    shuffle_questions = Column(Boolean, default=True)
    total_questions = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    item = relationship("LearningItem", back_populates="quiz")
    questions = relationship("Question", back_populates="quiz")
    results = relationship("QuizResult", back_populates="quiz")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    content = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)
    correct_option = Column(Integer, nullable=False)
    explanation = Column(Text, nullable=True)
    difficulty = Column(Enum("easy", "medium", "hard"), default="medium")
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    topic = relationship("Topic", back_populates="questions")


class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(Integer, ForeignKey("learning_items.id", ondelete="CASCADE"), nullable=False)
    started_at = Column(DateTime, server_default=func.now())
    ended_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, default=0)
    completion_rate = Column(Float, default=0.0)
    interaction_score = Column(Float, default=0.0)
    status = Column(Enum("in_progress", "completed", "abandoned"), default="in_progress")

    # Relationships
    user = relationship("User", back_populates="sessions")
    item = relationship("LearningItem", back_populates="sessions")


class FlashcardLog(Base):
    __tablename__ = "flashcard_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    flashcard_id = Column(Integer, ForeignKey("flashcards.id", ondelete="CASCADE"), nullable=False)
    result = Column(Enum("correct", "incorrect", "skipped"), nullable=False)
    response_time_ms = Column(Integer, default=0)
    answered_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="flashcard_logs")
    flashcard = relationship("Flashcard", back_populates="logs")


class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float, nullable=False, default=0)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, default=0)
    answers = Column(JSON, nullable=True)
    time_spent_seconds = Column(Integer, default=0)
    is_passed = Column(Boolean, default=False)
    taken_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="quiz_results")
    quiz = relationship("Quiz", back_populates="results")


class LearningProfile(Base):
    __tablename__ = "learning_profiles"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    topic_scores = Column(JSON, nullable=True)
    difficulty_distribution = Column(JSON, nullable=True)
    preferred_difficulty = Column(Enum("beginner", "intermediate", "advanced"), default="beginner")
    profile_vector = Column(JSON, nullable=True)
    total_study_hours = Column(Float, default=0.0)
    total_items_completed = Column(Integer, default=0)
    total_quizzes_taken = Column(Integer, default=0)
    avg_quiz_score = Column(Float, default=0.0)
    learning_streak = Column(Integer, default=1)
    is_onboarded = Column(Boolean, default=False)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(Integer, ForeignKey("learning_items.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float, nullable=False, default=0.0)
    reason = Column(String(500), nullable=True)
    rec_type = Column(Enum("content", "path", "review", "cold_start"), default="content")
    is_clicked = Column(Boolean, default=False)
    generated_at = Column(DateTime, server_default=func.now())
    clicked_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="recommendations")
    item = relationship("LearningItem", back_populates="recommendations")


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500), default="Lo trinh hoc cua toi")
    item_sequence = Column(JSON, nullable=True)
    progress_percent = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="learning_paths")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), default="info") # info, success, warning, error
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="notifications")


# --- SURVEY & ONBOARDING MODELS ---

class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum("draft", "published", "archived"), default="draft")
    is_active = Column(Boolean, default=False)
    version = Column(Integer, default=1)
    time_limit_minutes = Column(Integer, default=15)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    questions = relationship("SurveyQuestion", back_populates="survey", cascade="all, delete-orphan")
    attempts = relationship("SurveyAttempt", back_populates="survey", cascade="all, delete-orphan")


class SurveyQuestion(Base):
    __tablename__ = "survey_questions"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    question_type = Column(Enum("single_choice", "multiple_choice", "rating", "text"), nullable=False)
    category = Column(Enum("knowledge", "goal", "interest", "self_assessment"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    difficulty = Column(Enum("beginner", "intermediate", "advanced"), nullable=True)
    weight = Column(Float, default=1.0)
    is_required = Column(Boolean, default=True)
    order_index = Column(Integer, default=0)
    status = Column(Enum("active", "inactive"), default="active")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    survey = relationship("Survey", back_populates="questions")
    topic = relationship("Topic")
    options = relationship("SurveyOption", back_populates="question", cascade="all, delete-orphan")


class SurveyOption(Base):
    __tablename__ = "survey_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("survey_questions.id", ondelete="CASCADE"), nullable=False)
    content = Column(String(500), nullable=False)
    value = Column(String(255), nullable=True)  # For mapping to profile keys
    is_correct = Column(Boolean, default=False)
    score = Column(Float, default=0.0)
    order_index = Column(Integer, default=0)

    question = relationship("SurveyQuestion", back_populates="options")


class SurveyAttempt(Base):
    __tablename__ = "survey_attempts"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    started_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
    status = Column(Enum("in_progress", "completed", "abandoned"), default="in_progress")
    total_score = Column(Float, default=0.0)
    analysis_result = Column(JSON, nullable=True)

    survey = relationship("Survey", back_populates="attempts")
    user = relationship("User")
    answers = relationship("SurveyAnswer", back_populates="attempt", cascade="all, delete-orphan")


class SurveyAnswer(Base):
    __tablename__ = "survey_answers"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("survey_attempts.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("survey_questions.id", ondelete="CASCADE"), nullable=False)
    option_id = Column(Integer, ForeignKey("survey_options.id", ondelete="SET NULL"), nullable=True)
    text_value = Column(Text, nullable=True)
    score = Column(Float, default=0.0)

    attempt = relationship("SurveyAttempt", back_populates="answers")
    question = relationship("SurveyQuestion")
    option = relationship("SurveyOption")

