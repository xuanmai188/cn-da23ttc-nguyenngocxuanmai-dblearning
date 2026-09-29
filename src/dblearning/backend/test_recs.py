# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.ml.profile_builder import update_user_profile
from app.ml.recommender import generate_recommendations
from app.models.models import Recommendation, LearningItem

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

print("--- SQL LOVER (User 101) ---")
update_user_profile(db, 101)
recs = generate_recommendations(db, 101)
for r in recs:
    item = db.query(LearningItem).get(r.item_id)
    print(f"[{r.score:.2f}] {item.title}")

print("\n--- THEORY FAN (User 102) ---")
update_user_profile(db, 102)
recs = generate_recommendations(db, 102)
for r in recs:
    item = db.query(LearningItem).get(r.item_id)
    print(f"[{r.score:.2f}] {item.title}")

db.close()
