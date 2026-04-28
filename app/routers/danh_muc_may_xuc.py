from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.security import get_current_user
from models.user import User
from schemas.danh_muc_may_xuc import (
    DanhMucMayXucCreate,
    DanhMucMayXucUpdate,
    DanhMucMayXucResponse,
)
from services.danh_muc_may_xuc_service import (
    create_danh_muc_may_xuc,
    get_danh_muc_may_xuc,
    get_danh_muc_may_xucs,
    update_danh_muc_may_xuc,
    delete_danh_muc_may_xuc,
    delete_many_danh_muc_may_xuc,
)

router = APIRouter(prefix="/danh-muc-may-xuc", tags=["Danh Muc May Xuc"])


@router.post("/", response_model=DanhMucMayXucResponse, status_code=status.HTTP_201_CREATED)
def add_danh_muc_may_xuc(
    payload: DanhMucMayXucCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_danh_muc_may_xuc(db, payload)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[DanhMucMayXucResponse])
def list_danh_muc_may_xuc(db: Session = Depends(get_db)):
    return get_danh_muc_may_xucs(db)


@router.get("/{record_id}", response_model=DanhMucMayXucResponse)
def read_danh_muc_may_xuc(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_danh_muc_may_xuc(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return record


@router.put("/{record_id}", response_model=DanhMucMayXucResponse)
def update_danh_muc_may_xuc_endpoint(
    record_id: int,
    payload: DanhMucMayXucUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_danh_muc_may_xuc(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return update_danh_muc_may_xuc(db, record, payload)


@router.delete("/{record_id}")
def delete_danh_muc_may_xuc_endpoint(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_danh_muc_may_xuc(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    delete_danh_muc_may_xuc(db, record)
    return {"message": "deleted"}


@router.delete("/")
def delete_many_danh_muc_may_xuc_endpoint(
    ids: List[int] = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_many_danh_muc_may_xuc(db, ids)
    return {"deleted_count": len(deleted)}
