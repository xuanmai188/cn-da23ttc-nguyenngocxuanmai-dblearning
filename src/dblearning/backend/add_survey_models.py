file_path = "D:/DemoCN2026/dblearning/backend/app/models/models.py"

survey_models = """

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

"""

with open(file_path, "a", encoding="utf-8") as f:
    f.write(survey_models)
print("Survey models appended successfully.")
