from sqlalchemy import create_engine, text
import os

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    db_url = "mysql+pymysql://dbuser:dbpassword@localhost:3306/dblearning"
engine = create_engine(db_url)
with engine.connect() as conn:
    conn.execute(text("INSERT INTO learning_sessions (user_id, item_id, started_at, duration_seconds, completion_rate, status) VALUES (103, 1, DATE_SUB(NOW(), INTERVAL 1 DAY), 600, 1.0, 'completed')"))
    conn.execute(text("INSERT INTO learning_sessions (user_id, item_id, started_at, duration_seconds, completion_rate, status) VALUES (103, 2, NOW(), 600, 1.0, 'completed')"))
    conn.commit()
print("Sessions added")
