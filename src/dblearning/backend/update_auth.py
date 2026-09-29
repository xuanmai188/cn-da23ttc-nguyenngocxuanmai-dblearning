file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/auth.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add UserUpdate import
if "UserUpdate" not in content:
    content = content.replace(
        "from app.schemas.user import UserCreate, User as UserSchema, Token, ForgotPasswordRequest, ResetPasswordRequest",
        "from app.schemas.user import UserCreate, User as UserSchema, Token, ForgotPasswordRequest, ResetPasswordRequest, UserUpdate"
    )

new_endpoint = """
@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_active_user)
):
    \"\"\"
    Cập nhật thông tin cá nhân.
    \"\"\"
    if user_in.full_name is not None:
        current_user.full_name = user_in.full_name
    if user_in.phone_number is not None:
        current_user.phone_number = user_in.phone_number
    if user_in.avatar_url is not None:
        current_user.avatar_url = user_in.avatar_url
    if user_in.password is not None:
        current_user.password_hash = security.get_password_hash(user_in.password)
    
    # We could allow email update here if needed, but let's keep it out unless requested
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
"""

if "@router.put(\"/me\"" not in content:
    content += "\n" + new_endpoint

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Added PUT /api/auth/me to auth.py")
