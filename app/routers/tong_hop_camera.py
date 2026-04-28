from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.security import get_current_user
from models.user import User
from schemas.tong_hop_camera import (
    TongHopCameraCreate,
    TongHopCameraUpdate,
    TongHopCameraResponse,
)
from services.tong_hop_camera_service import (
    create_tong_hop_camera,
    get_tong_hop_camera,
    get_tong_hop_cameras,
    update_tong_hop_camera,
    delete_tong_hop_camera,
)

router = APIRouter(prefix="/tong-hop-camera", tags=["Tong Hop Camera"])


@router.post("/", response_model=TongHopCameraResponse)
def add_tong_hop_camera(
    payload: TongHopCameraCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return create_tong_hop_camera(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[TongHopCameraResponse])
def list_tong_hop_cameras(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_tong_hop_cameras(db)


@router.get("/{record_id}", response_model=TongHopCameraResponse)
def read_tong_hop_camera(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = get_tong_hop_camera(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return record


@router.put("/{record_id}", response_model=TongHopCameraResponse)
def update_tong_hop_camera_endpoint(
    record_id: int,
    payload: TongHopCameraUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = get_tong_hop_camera(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return update_tong_hop_camera(db, record, payload)


@router.delete("/{record_id}")
def delete_tong_hop_camera_endpoint(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = get_tong_hop_camera(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    delete_tong_hop_camera(db, record)
    return {"message": "deleted"}
