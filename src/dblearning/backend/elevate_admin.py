from sqlalchemy import create_engine, text
import os

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    db_url = "mysql+pymysql://dbuser:dbpassword@localhost:3306/dblearning"
engine = create_engine(db_url)
with engine.connect() as conn:
    conn.execute(text("UPDATE users SET role='admin' WHERE email='nguyenngocxuanmai188@gmail.com'"))
    conn.commit()
print("User elevated to admin")
