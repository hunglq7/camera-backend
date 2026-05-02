from typing import List, Optional
from sqlalchemy.orm import Session
from models.user import User
from schemas.auth import UserRegister
from schemas.user import UserUpdate
from services.auth_service import hash_password
from fastapi import HTTPException, status


def get_users(db: Session, skip: int = 0, limit: int = 100):
    query = db.query(User)
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    return users, total


def create_user(db: Session, user_register: UserRegister) -> User:
    existing_user = db.query(User).filter(
        (User.username == user_register.username) | (User.email == user_register.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    new_user = User(
        username=user_register.username,
        email=user_register.email,
        hashed_password=hash_password(user_register.password),
        roles=",".join(user_register.roles) if user_register.roles else "user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.phone is not None:
        user.phone = user_update.phone
    if user_update.avatar is not None:
        user.avatar = user_update.avatar
    if user_update.password is not None:
        user.hashed_password = hash_password(user_update.password)
    if user_update.roles is not None and user_update.roles:
        user.roles = ",".join(user_update.roles)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> int:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user)
    db.commit()
    return user_id


def delete_users(db: Session, ids: List[int]) -> int:
    deleted = db.query(User).filter(User.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    return deleted
