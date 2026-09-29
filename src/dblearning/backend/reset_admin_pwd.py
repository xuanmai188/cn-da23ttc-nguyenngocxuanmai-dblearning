from sqlalchemy import create_engine, text
from passlib.context import CryptContext
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("admin")

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    db_url = "mysql+pymysql://dbuser:dbpassword@localhost:3306/dblearning?charset=utf8mb4"

engine = create_engine(db_url)
with engine.connect() as conn:
    conn.execute(text(f"UPDATE users SET password_hash = '{hashed_password}' WHERE email = 'admin@dblearning.edu.vn'"))
    conn.commit()
    print("Admin password updated to 'admin'")
