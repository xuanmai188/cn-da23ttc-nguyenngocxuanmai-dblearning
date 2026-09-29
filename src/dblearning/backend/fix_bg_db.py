file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/learning.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_func = """
def run_profile_update(user_id: int):
    db = next(deps.get_db())
    try:
        update_user_profile(db, user_id)
    finally:
        db.close()
"""
if "def run_profile_update" not in content:
    content = content.replace("router = APIRouter()", new_func + "\nrouter = APIRouter()")

content = content.replace("background_tasks.add_task(update_user_profile, db=db, user_id=current_user.id)", "background_tasks.add_task(run_profile_update, user_id=current_user.id)")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed background task DB session")
