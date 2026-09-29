from sqlalchemy import create_engine, text
import os
db_url = os.environ.get("DATABASE_URL")
engine = create_engine(db_url)
with engine.connect() as conn:
    r = conn.execute(text("SHOW COLUMNS FROM recommendations"))
    for row in r:
        print(row)
