import os
from sqlalchemy import create_engine, text

db_url = os.environ.get("DATABASE_URL", "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

with engine.connect() as conn:
    # Xoa recommendations cho user 103 (tai khoan moi) de buoc gen lai
    conn.execute(text("DELETE FROM recommendations WHERE user_id = 103"))
    # Xoa luon profile de force cold start
    conn.execute(text("DELETE FROM learning_profiles WHERE user_id = 103"))
    conn.commit()
    print("Cleared recommendations and profile for user 103")
    
    # Kiem tra lai
    result = conn.execute(text("SELECT COUNT(*) FROM recommendations WHERE user_id = 103"))
    print(f"Remaining recs for user 103: {result.fetchone()[0]}")
