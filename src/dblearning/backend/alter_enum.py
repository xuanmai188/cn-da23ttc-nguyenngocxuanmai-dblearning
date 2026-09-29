from sqlalchemy import create_engine, text
import os
db_url = os.environ.get("DATABASE_URL")
engine = create_engine(db_url)
with engine.connect() as conn:
    # Add 'cold_start' to the enum
    conn.execute(text("ALTER TABLE recommendations MODIFY rec_type ENUM('content','path','review','cold_start') DEFAULT 'content'"))
    conn.commit()
    print("Added cold_start to rec_type enum")
