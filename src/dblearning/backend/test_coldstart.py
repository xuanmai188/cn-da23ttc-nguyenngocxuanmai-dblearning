import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.ml.recommender import generate_recommendations, generate_cold_start_recommendations
from app.ml.profile_builder import update_user_profile
from app.models.models import Recommendation, LearningItem

db_url = os.environ.get("DATABASE_URL", "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

print("--- TEST COLD START for User 103 (brand new user) ---")
recs = generate_cold_start_recommendations(db, 103)
for r in recs:
    item = db.get(LearningItem, r.item_id)
    print(f"  [{item.content_type}] [{item.difficulty}] {item.title}")

db.close()
