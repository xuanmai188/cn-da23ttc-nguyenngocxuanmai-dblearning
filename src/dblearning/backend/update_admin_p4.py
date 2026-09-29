file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_code = """from pydantic import BaseModel
from typing import Optional
from app.core.security import get_password_hash

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    phone_number: Optional[str] = None
    role: str = "student"

class UserUpdate(BaseModel):
    full_name: str
    phone_number: Optional[str] = None
    role: str

@router.post("/users")
def create_user(
    user_in: UserCreate,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")
    
    new_user = User(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        phone_number=user_in.phone_number,
        role=user_in.role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    return {"message": "Tạo thành công"}

@router.put("/users/{user_id}")
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
    db.commit()
    return {"message": "Cập nhật thành công"}

@router.put("/users/{user_id}/reset-password")
def reset_user_password(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
        
    user.password_hash = get_password_hash("123456")
    db.commit()
    return {"message": "Mật khẩu đã được đặt lại thành 123456"}
"""

content = content + "\n" + new_code

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated admin.py with Phase 4 APIs")
