file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace get_recent_activities signature and query limit
old_sig = """def get_recent_activities(
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:"""
new_sig = """def get_recent_activities(
    limit: int = 5,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:"""
content = content.replace(old_sig, new_sig)

content = content.replace(".limit(5).all()", ".limit(limit).all()")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated backend admin.py to support limit parameter for recent activities")
