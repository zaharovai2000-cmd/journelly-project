from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re


class RegisterRequest(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if v is not None:
            # Приводим к формату +7XXXXXXXXXX
            cleaned = re.sub(r"[^\d+]", "", v)
            if not re.match(r"^\+?[78]\d{10}$", cleaned):
                raise ValueError("Некорректный номер телефона")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Имя должно содержать минимум 2 символа")
        return v.strip()

    def model_post_init(self, __context):
        if not self.email and not self.phone:
            raise ValueError("Укажите email или номер телефона")


class LoginRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str

    def model_post_init(self, __context):
        if not self.email and not self.phone:
            raise ValueError("Укажите email или номер телефона")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # секунд до истечения access токена


class RefreshRequest(BaseModel):
    refresh_token: str