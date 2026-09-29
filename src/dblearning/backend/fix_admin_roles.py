from sqlalchemy import create_engine, text
import os

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    db_url = "mysql+pymysql://dbuser:dbpassword@localhost:3306/dblearning?charset=utf8mb4"

engine = create_engine(db_url)
with engine.connect() as conn:
    # 1. Re-create the dedicated admin account
    conn.execute(text("""
        INSERT IGNORE INTO users (email, password_hash, full_name, role)
        VALUES ('admin@dblearning.edu.vn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMaijsWGUxOaT3pS9pWtGXmhIO', 'Quản trị viên Hệ thống', 'admin')
    """))
    
    # 2. Downgrade nguyenngocxuanmai188@gmail.com back to student
    conn.execute(text("""
        UPDATE users SET role = 'student' WHERE email = 'nguyenngocxuanmai188@gmail.com'
    """))
    
    conn.commit()
    print("Fixed roles successfully.")
