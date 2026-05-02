from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import get_current_user
from models.user import User
from schemas.danh_muc_dien_thoai import (
    DanhMucDienThoaiCreate,
    DanhMucDienThoaiUpdate,
    DanhMucDienThoaiResponse,
)
from services.danh_muc_dien_thoai_service import (
    create_danh_muc_dien_thoai,
    get_danh_muc_dien_thoai,
    get_danh_muc_dien_thoais,
    update_danh_muc_dien_thoai,
    delete_danh_muc_dien_thoai,
    delete_many_danh_muc_dien_thoai,
)

router = APIRouter(prefix="/danh-muc-dien-thoai", tags=["Danh Muc Dien Thoai"])

@router.post("/", response_model=DanhMucDienThoaiResponse, status_code=status.HTTP_201_CREATED)
def add_danh_muc_dien_thoai(
    payload: DanhMucDienThoaiCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_danh_muc_dien_thoai(db, payload)

@router.get("/", response_model=List[DanhMucDienThoaiResponse])
def list_danh_muc_dien_thoai(db: Session = Depends(get_db)):
    return get_danh_muc_dien_thoais(db)

@router.get("/{record_id}", response_model=DanhMucDienThoaiResponse)
def read_danh_muc_dien_thoai(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_danh_muc_dien_thoai(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return record

@router.put("/{record_id}", response_model=DanhMucDienThoaiResponse)
def update_danh_muc_dien_thoai_endpoint(
    record_id: int,
    payload: DanhMucDienThoaiUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_danh_muc_dien_thoai(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return update_danh_muc_dien_thoai(db, record, payload)

@router.delete("/{record_id}")
def delete_danh_muc_dien_thoai_endpoint(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_danh_muc_dien_thoai(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    delete_danh_muc_dien_thoai(db, record)
    return {"message": "deleted"}

@router.delete("/")
def delete_many_danh_muc_dien_thoai_endpoint(
    ids: List[int] = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_many_danh_muc_dien_thoai(db, ids)
    return {"deleted_count": len(deleted)}