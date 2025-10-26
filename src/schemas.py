"""Pydantic schemas for User.

Note: This file uses Pydantic v2 style configuration.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------- Base ----------
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="nimakaydan@gmail.com")
    name: str = Field(..., min_length=1, max_length=100, description="Nima Kaydan")
    age: Optional[int] = Field(None, ge=0, le=150, description="42")


# ---------- Create / Update payloads ----------
class UserCreate(UserBase):
    """Payload ایجاد کاربر (client → server)"""

    pass


class UserUpdate(BaseModel):
    """Payload آپدیت کاربر (Patch/Put)"""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)


# ---------- Read models (server → client) ----------
class UserRead(UserBase):
    """خروجی API برای خواندن/لیست‌کردن کاربر"""

    id: int
    created_at: datetime

    # به Pydانتیک می‌گوید که می‌تواند از آبجکت‌های ORM (SQLAlchemy) هم بخواند
    # (معادل orm_mode=True در Pydantic v1)
    model_config = ConfigDict(from_attributes=True)
