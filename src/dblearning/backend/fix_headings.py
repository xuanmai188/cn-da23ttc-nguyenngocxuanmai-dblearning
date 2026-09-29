# -*- coding: utf-8 -*-
import os
import re
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

with engine.connect() as conn:
    result = conn.execute(text("SELECT id, content_body FROM learning_items WHERE content_type='document'"))
    for row in result.fetchall():
        item_id = row[0]
        body = row[1]
        if not body:
            continue
            
        # Remove "PHẦN X: " or "Phần X: " from headings
        body = re.sub(r"##\s*PHẦN\s*\d+\s*:\s*", "## ", body, flags=re.IGNORECASE)
        
        # Remove numbered subheadings like "3.1. " or "4.2 "
        body = re.sub(r"###\s*\d+\.\d+\.?\s*", "### ", body)
        
        conn.execute(text("UPDATE learning_items SET content_body = :body WHERE id = :id"), {"body": body, "id": item_id})
    
    conn.commit()

print("Headings fixed successfully!")
