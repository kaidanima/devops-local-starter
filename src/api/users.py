# src/api/users.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.db import get_db
from src import models
from src.schemas import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)) -> List[models.User]:
    """برگرداندن همه‌ی کاربران (ساده و بدون pagination برای شروع)"""
    return db.query(models.User).order_by(models.User.id.asc()).all()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> models.User:
    """ایجاد کاربر جدید؛ اگر ایمیل تکراری باشد 409 برمی‌گردانیم"""
    user = models.User(email=payload.email, name=payload.name, age=payload.age)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email already exists",
        )
    db.refresh(user)
    return user