from sqlalchemy import create_engine, text
import os
db_url = os.environ.get("DATABASE_URL")
engine = create_engine(db_url)
with engine.connect() as conn:
    print("--- Flashcards for item 8 ---")
    r = conn.execute(text("SELECT * FROM flashcards WHERE item_id=8"))
    for row in r:
        print(row)
        
    print("--- Quiz for item 9 ---")
    r = conn.execute(text("SELECT * FROM quizzes WHERE item_id=9"))
    for row in r:
        print(row)
        
    print("--- Questions for quiz of item 9 ---")
    r = conn.execute(text("SELECT * FROM questions WHERE quiz_id IN (SELECT id FROM quizzes WHERE item_id=9)"))
    for row in r:
        print(row)
