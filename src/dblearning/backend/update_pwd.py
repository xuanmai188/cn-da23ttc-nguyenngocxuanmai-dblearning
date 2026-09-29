import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

with engine.connect() as conn:
    conn.execute(text("UPDATE users SET password_hash = :h WHERE id IN (101, 102)"), {'h': '/L48yV/1Oc0Spjy8Oy8hpSQRtOZTiiTw2A/Lkn4V6HhoYFSa'})
    conn.commit()
print("Passwords updated!")
