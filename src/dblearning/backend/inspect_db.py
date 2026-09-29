import os
from sqlalchemy import create_engine, text
db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)
with engine.connect() as conn:
    print("=== TABLES ===")
    tables = conn.execute(text("SHOW TABLES")).fetchall()
    for t in tables:
        print(t[0])
    
    print("\n=== USERS ROLES ===")
    roles = conn.execute(text("SELECT role, COUNT(*) FROM users GROUP BY role")).fetchall()
    for r in roles:
        print(r[0], r[1])
