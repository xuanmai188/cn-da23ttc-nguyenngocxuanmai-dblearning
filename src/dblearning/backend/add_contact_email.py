import os
import sys

# Add backend dir to python path
sys.path.append("D:/DemoCN2026/dblearning/backend")

from app.core.database import SessionLocal, engine
from sqlalchemy import text

db = SessionLocal()
try:
    # Check if contact_email exists
    res = db.execute(text("SHOW COLUMNS FROM users LIKE 'contact_email'")).fetchone()
    if not res:
        print("Adding contact_email column to users table...")
        db.execute(text("ALTER TABLE users ADD COLUMN contact_email VARCHAR(255) NULL"))
        db.commit()
        print("Successfully added contact_email column.")
    else:
        print("Column contact_email already exists.")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
