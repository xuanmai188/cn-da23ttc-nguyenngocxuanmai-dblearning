import os
from sqlalchemy import create_engine, text
db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)
with engine.connect() as conn:
    tables = conn.execute(text("SHOW TABLES")).fetchall()
    print("Tables in DB:")
    for t in tables:
        print(f"- {t[0]}")
