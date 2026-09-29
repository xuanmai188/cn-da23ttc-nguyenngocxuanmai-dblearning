# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

with engine.connect() as conn:
    result = conn.execute(text('SELECT title FROM learning_items WHERE content_type="document" AND content_body NOT LIKE "%PHẦN 3%" AND content_body NOT LIKE "%Chuyên sâu Kỹ thuật%" AND content_body NOT LIKE "%BÀI HỌC TOÀN DIỆN%"'))
    items = result.fetchall()
    
    print("Items not fully MEGA-upgraded:")
    for item in items:
        print(f"- {item[0]}")
