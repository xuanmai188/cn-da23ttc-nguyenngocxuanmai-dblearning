file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

old_update_user = """@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
        
    user.full_name = user_in.full_name
    user.phone_number = user_in.phone_number
    user.role = user_in.role
    user.contact_email = user_in.contact_email
    db.commit()
    return {"message": "Cập nhật thành công"}"""

new_update_user = """@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
        
    update_data = user_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
        
    db.commit()
    return {"message": "Cập nhật thành công"}"""

content = content.replace(old_update_user, new_update_user)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated admin.py update_user endpoint")
