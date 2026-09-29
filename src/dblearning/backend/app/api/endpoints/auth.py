from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.api import deps
from app.models.models import User, LearningProfile
from app.schemas.user import UserCreate, User as UserSchema, Token, ForgotPasswordRequest, ResetPasswordRequest, UserUpdate

router = APIRouter()


@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
):
    """
    Đăng ký tài khoản mới.
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="Email đã được sử dụng",
        )
    
    user = User(
        email=user_in.email,
        password_hash=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        avatar_url=user_in.avatar_url,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Khởi tạo Learning Profile trống cho user mới
    profile = LearningProfile(user_id=user.id)
    db.add(profile)
    db.commit()

    return user


@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Đăng nhập bằng email và password. Trả về access token.
    (Lưu ý: OAuth2PasswordRequestForm dùng username field cho email)
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Tài khoản đã bị khóa")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserSchema)
def read_users_me(
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Lấy thông tin người dùng đang đăng nhập.
    """
    return current_user


@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(deps.get_db)
):
    """
    Yêu cầu lấy lại mật khẩu.
    Chỉ trả về reset_link (để test) thay vì gửi email.
    """
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        # Trả về thành công ảo để chống dò email
        return {"message": "Nếu email hợp lệ, một link khôi phục đã được gửi."}

    # Tạo token với hạn 15 phút, type="reset_password"
    expires = timedelta(minutes=15)
    reset_token = security.create_access_token(
        data={"sub": str(user.id), "type": "reset_password"}, 
        expires_delta=expires
    )
    
    # Ở môi trường thực tế, reset_link này sẽ được gửi qua Email
    reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
    
    return {
        "message": "Nếu email hợp lệ, một link khôi phục đã được gửi.",
        "debug_reset_link": reset_link
    }


@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(deps.get_db)
):
    """
    Khôi phục mật khẩu dựa vào token
    """
    try:
        payload = security.decode_token(request.token)
        if payload.get("type") != "reset_password":
            raise HTTPException(status_code=400, detail="Token không hợp lệ")
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=400, detail="Token không hợp lệ")
            
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="Người dùng không tồn tại")
            
        user.password_hash = security.get_password_hash(request.new_password)
        db.commit()
        
        return {"message": "Mật khẩu đã được khôi phục thành công"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="Token không hợp lệ hoặc đã hết hạn")


@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Cập nhật thông tin cá nhân.
    """
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
