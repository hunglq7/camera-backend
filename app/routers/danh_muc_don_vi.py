from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.security import get_current_user
from models.user import User
from schemas.danh_muc_don_vi import (
    DanhmucDonViCreate,
    DanhmucDonViUpdate,
    DanhmucDonViResponse,
)
from services.danh_muc_don_vi_service import (
    create_danh_muc_don_vi,
    get_danh_muc_don_vi,
    get_danh_muc_don_vis,
    update_danh_muc_don_vi,
    delete_danh_muc_don_vi,
   delete_many_danh_muc_don_vi
)

router = APIRouter(prefix="/danh-muc-don-vi", tags=["Danh Muc Don Vi"])

@router.post("/", response_model=DanhmucDonViResponse, status_code=status.HTTP_201_CREATED)
def add_danh_muc_don_vi(
    payload: DanhmucDonViCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_danh_muc_don_vi(db, payload)

@router.get("/", response_model=List[DanhmucDonViResponse])
def list_danh_muc_don_vi(db: Session = Depends(get_db)):
    return get_danh_muc_don_vis(db)

@router.get("/{record_id}", response_model=DanhmucDonViResponse)
def read_danh_muc_don_vi(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_danh_muc_don_vi(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return record

@router.put("/{record_id}", response_model=DanhmucDonViResponse)
def update_danh_muc_don_vi_endpoint(
    record_id: int,
    payload: DanhmucDonViUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_danh_muc_don_vi(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return update_danh_muc_don_vi(db, record, payload)

@router.delete("/{record_id}")
def delete_danh_muc_don_vi_endpoint(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_danh_muc_don_vi(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    delete_danh_muc_don_vi(db, record)
    return {"message": "deleted"}

@router.delete("/")
def delete_many_danh_muc_don_vi_endpoint(
    ids: List[int] = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_many_danh_muc_don_vi(db, ids)
    return {"deleted_count": len(deleted)}