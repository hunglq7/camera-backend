from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import get_current_user
from models.user import User
from schemas.danh_muc_camera import (
    DanhMucCameraCreate,
    DanhMucCameraUpdate,
    DanhMucCameraResponse,
)
from services.danh_muc_camera_service import (
    create_danh_muc_camera,
    get_danh_muc_camera,
    get_danh_muc_cameras,
    update_danh_muc_camera,
    delete_danh_muc_camera,
    delete_many_danh_muc_camera,
)

router = APIRouter(prefix="/danh-muc-camera", tags=["Danh Muc Camera"])

@router.post("/", response_model=DanhMucCameraResponse, status_code=status.HTTP_201_CREATED)
def add_danh_muc_camera(
    payload: DanhMucCameraCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_danh_muc_camera(db, payload)

@router.get("/", response_model=List[DanhMucCameraResponse])
def list_danh_muc_camera(db: Session = Depends(get_db)):
    return get_danh_muc_cameras(db)

@router.get("/{record_id}", response_model=DanhMucCameraResponse)
def read_danh_muc_camera(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_danh_muc_camera(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return record

@router.put("/{record_id}", response_model=DanhMucCameraResponse)
def update_danh_muc_camera_endpoint(
    record_id: int,
    payload: DanhMucCameraUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_danh_muc_camera(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return update_danh_muc_camera(db, record, payload)

@router.delete("/{record_id}")
def delete_danh_muc_camera_endpoint(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_danh_muc_camera(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    delete_danh_muc_camera(db, record)
    return {"message": "deleted"}

@router.delete("/")
def delete_many_danh_muc_camera_endpoint(
    ids: List[int] = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_many_danh_muc_camera(db, ids)
    return {"deleted_count": len(deleted)}