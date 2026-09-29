import os
from sqlalchemy import create_engine, text

db_url = os.environ.get("DATABASE_URL", "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

with engine.connect() as conn:
    # Lay user id moi tao
    result = conn.execute(text("SELECT id, email FROM users ORDER BY id DESC LIMIT 5"))
    for row in result:
        print(f"User: id={row[0]}, email={row[1]}")
    print("---")
    # Xoa recommendations cu
    result2 = conn.execute(text("SELECT user_id, COUNT(*) as cnt FROM recommendations GROUP BY user_id"))
    for row in result2:
        print(f"user_id={row[0]}: {row[1]} recommendations")
