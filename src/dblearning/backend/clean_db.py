from sqlalchemy import create_engine, text
import os

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    db_url = "mysql+pymysql://dbuser:dbpassword@localhost:3306/dblearning"

engine = create_engine(db_url)
with engine.connect() as conn:
    # Get user 103's ID just to be safe
    res = conn.execute(text("SELECT id FROM users WHERE email='nguyenngocxuanmai188@gmail.com'"))
    row = res.fetchone()
    if row:
        user_id = row[0]
        # Delete from child tables first for all OTHER users
        conn.execute(text(f"DELETE FROM learning_sessions WHERE user_id != {user_id}"))
        conn.execute(text(f"DELETE FROM learning_profiles WHERE user_id != {user_id}"))
        conn.execute(text(f"DELETE FROM flashcard_logs WHERE user_id != {user_id}"))
        conn.execute(text(f"DELETE FROM quiz_results WHERE user_id != {user_id}"))
        conn.execute(text(f"DELETE FROM recommendations WHERE user_id != {user_id}"))
        # Delete other users
        conn.execute(text(f"DELETE FROM users WHERE id != {user_id}"))
        conn.commit()
        print("Database cleaned. Only user 103 remains.")
    else:
        print("User not found!")
