from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.models.models import Quiz
from app.schemas.quiz import Quiz as QuizSchema

db_url = os.environ.get("DATABASE_URL")
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

quiz = db.query(Quiz).filter(Quiz.item_id == 4).first()
questions = quiz.questions
print(len(questions))
try:
    quiz_data = QuizSchema.model_validate(quiz)
    print(quiz_data.model_dump())
except Exception as e:
    print("Error mapping schema:", e)
