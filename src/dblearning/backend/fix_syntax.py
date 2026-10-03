file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

bad_block = """) -> Any:
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    topic_id: Optional[int] = None,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:"""

content = content.replace(bad_block, ") -> Any:")

bad_block2 = """) -> Any:
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    item_id: Optional[int] = None,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:"""

content = content.replace(bad_block2, ") -> Any:")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed duplicate argument syntax errors")
