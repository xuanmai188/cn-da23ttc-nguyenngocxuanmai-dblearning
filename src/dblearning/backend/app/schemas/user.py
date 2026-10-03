import re
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


# Shared properties
class UserBase(BaseModel):
    email: str
    full_name: str
    contact_email: Optional[str] = None
    avatar_url: Optional[str] = None
    phone_number: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    role: str = "student"

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Mật khẩu phải có ít nhất 8 ký tự')
        if not re.search(r"[A-Z]", v):
            raise ValueError('Mật khẩu phải có ít nhất 1 chữ hoa')
        if not re.search(r"[a-z]", v):
            raise ValueError('Mật khẩu phải có ít nhất 1 chữ thường')
        if not re.search(r"\d", v):
            raise ValueError('Mật khẩu phải có ít nhất 1 chữ số')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError('Mật khẩu phải có ít nhất 1 ký tự đặc biệt')
        return v

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Mật khẩu phải có ít nhất 8 ký tự')
        if not re.search(r"[A-Z]", v):
            raise ValueError('Mật khẩu phải có ít nhất 1 chữ hoa')
        if not re.search(r"[a-z]", v):
            raise ValueError('Mật khẩu phải có ít nhất 1 chữ thường')
        if not re.search(r"\d", v):
            raise ValueError('Mật khẩu phải có ít nhất 1 chữ số')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError('Mật khẩu phải có ít nhất 1 ký tự đặc biệt')
        return v

# Properties to receive via API on update
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    contact_email: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    avatar_url: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if len(v) < 8:
                raise ValueError('Mật khẩu phải có ít nhất 8 ký tự')
            if not re.search(r"[A-Z]", v):
                raise ValueError('Mật khẩu phải có ít nhất 1 chữ hoa')
            if not re.search(r"[a-z]", v):
                raise ValueError('Mật khẩu phải có ít nhất 1 chữ thường')
            if not re.search(r"\d", v):
                raise ValueError('Mật khẩu phải có ít nhất 1 chữ số')
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
                raise ValueError('Mật khẩu phải có ít nhất 1 ký tự đặc biệt')
        return v


class UserInDBBase(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
