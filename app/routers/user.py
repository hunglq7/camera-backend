from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from schemas.auth import AdminUserRegister, UserResponse
from schemas.user import UserListResponse, UserUpdate, BulkDeleteRequest
from services.user_service import get_users, create_user, update_user, delete_user, delete_users
from models.user import User

router = APIRouter(prefix="/users", tags=["User Management"])


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    roles = [role.strip().lower() for role in (current_user.roles or "").split(",") if role.strip()]
    if "admin" not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


@router.get("/", response_model=UserListResponse)
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    users, total = get_users(db, skip=skip, limit=limit)
    return {"list": users, "total": total}


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_item(user_register: AdminUserRegister, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return create_user(db, user_register)


@router.put("/{user_id}", response_model=UserResponse)
def update_user_item(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return update_user(db, user_id, user_update)


@router.delete("/{user_id}")
def delete_user_item(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    deleted_id = delete_user(db, user_id)
    return {"deleted": deleted_id}


@router.delete("/")
def delete_users_batch(payload: BulkDeleteRequest, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    deleted_count = delete_users(db, payload.ids)
    return {"deleted": deleted_count}
