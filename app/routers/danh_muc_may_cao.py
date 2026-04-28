from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.security import get_current_user
from models.user import User
from schemas.danh_muc_may_cao import (
    DanhMucMayCaoCreate,
    DanhMucMayCaoUpdate,
    DanhMucMayCaoResponse,
)
from services.danh_muc_may_cao_service import (
    create_danh_muc_may_cao,
    get_danh_muc_may_cao,
    get_danh_muc_may_caos,
    update_danh_muc_may_cao,
    delete_danh_muc_may_cao,
    delete_many_danh_muc_may_cao,
)

router = APIRouter(prefix="/danh-muc-may-cao", tags=["Danh Muc May Cao"])

@router.post("/", response_model=DanhMucMayCaoResponse, status_code=status.HTTP_201_CREATED)
def add_danh_muc_may_cao(
    payload: DanhMucMayCaoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_danh_muc_may_cao(db, payload)

@router.get("/", response_model=List[DanhMucMayCaoResponse])
def list_danh_muc_may_cao(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_danh_muc_may_caos(db)

@router.get("/{record_id}", response_model=DanhMucMayCaoResponse)
def read_danh_muc_may_cao(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_danh_muc_may_cao(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return record

@router.put("/{record_id}", response_model=DanhMucMayCaoResponse)
def update_danh_muc_may_cao_endpoint(
    record_id: int,
    payload: DanhMucMayCaoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_danh_muc_may_cao(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return update_danh_muc_may_cao(db, record, payload)

@router.delete("/{record_id}")
def delete_danh_muc_may_cao_endpoint(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_danh_muc_may_cao(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    delete_danh_muc_may_cao(db, record)
    return {"message": "deleted"}

@router.delete("/")
def delete_many_danh_muc_may_cao_endpoint(
    ids: List[int] = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_many_danh_muc_may_cao(db, ids)
    return {"deleted_count": len(deleted)}