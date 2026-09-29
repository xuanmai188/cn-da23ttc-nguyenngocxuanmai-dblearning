from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.models import User
from app.schemas.user import TokenPayload
import traceback

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/auth/login")

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        print("RECEIVED TOKEN:", token); payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise Exception("user_id is None")
        token_data = TokenPayload(sub=int(user_id))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Decode error: {repr(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    try:
        user = db.query(User).filter(User.id == token_data.sub).first()
        if user is None:
            raise Exception("user not found in db")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Tài khoản đã bị khóa")
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"DB error: {repr(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Tài khoản đã bị khóa")
    return current_user

def get_current_active_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Người dùng không có quyền truy cập này"
        )
    return current_user

