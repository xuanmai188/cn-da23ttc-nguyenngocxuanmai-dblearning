# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

with engine.connect() as conn:
    result = conn.execute(text('SELECT title FROM learning_items WHERE content_type="document" AND content_body LIKE "%Nội dung chi tiết được biên soạn%"'))
    items = result.fetchall()
    
    print("Items needing update:")
    for item in items:
        print(f"- {item[0]}")
