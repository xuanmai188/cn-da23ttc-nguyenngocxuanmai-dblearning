import os
from sqlalchemy import create_engine, text
db_url = os.environ.get('DATABASE_URL', 'mysql+pymysql://dbuser:dbpassword@mysql:3306/dblearning')
engine = create_engine(db_url)
with engine.connect() as conn:
    conn.execute(text("UPDATE users SET email = SUBSTRING_INDEX(email, '@', 1) WHERE email LIKE '%@%';"))
    conn.commit()
print('Database updated')
