file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/learning.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add BackgroundTasks import if not present
if "BackgroundTasks" not in content:
    content = content.replace("from fastapi import APIRouter, Depends, HTTPException", "from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks")
elif "BackgroundTasks" not in content.split("from fastapi")[1].split("\n")[0]:
    # It might be in recommendation.py but not here.
    content = content.replace("from fastapi import APIRouter, Depends, HTTPException", "from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks")

# Add update_user_profile import
if "update_user_profile" not in content:
    content = content.replace("from app.schemas.learning", "from app.ml.profile_builder import update_user_profile\nfrom app.schemas.learning")

# Replace update_learning_session signature
old_sig = """def update_learning_session(
    session_id: int,
    session_in: LearningSessionUpdate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):"""
new_sig = """def update_learning_session(
    session_id: int,
    session_in: LearningSessionUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):"""
content = content.replace(old_sig, new_sig)

# Uncomment the background task line
old_task = """    # Trigger cập nhật profile ở background (sẽ implement sau)
    # BackgroundTasks.add_task(update_user_profile, user_id=current_user.id)"""
new_task = """    # Cập nhật profile sau khi hoàn thành
    background_tasks.add_task(update_user_profile, db=db, user_id=current_user.id)"""
if old_task in content:
    content = content.replace(old_task, new_task)
else:
    # Maybe the comment is slightly different
    content = content.replace("# BackgroundTasks.add_task(update_user_profile, user_id=current_user.id)", "background_tasks.add_task(update_user_profile, db=db, user_id=current_user.id)")
    
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("learning.py updated")
