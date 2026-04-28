from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.camera import Camera
from schemas.camera import CameraCreate, CameraResponse
from services.camera_service import create_camera, scan_camera

router = APIRouter(prefix="/cameras", tags=["Camera Management"])


@router.post("/", response_model=CameraResponse)
def add_camera(
    camera: CameraCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return create_camera(db, camera)
    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))


@router.get("/", response_model=List[CameraResponse])
def list_cameras(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Camera).all()


@router.put("/{camera_id}/scan", response_model=CameraResponse)
def scan(
    camera_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cam = db.query(Camera).filter(Camera.id == camera_id).first()
    if not cam:
        raise HTTPException(404, "Not found")

    return scan_camera(db, cam)


@router.delete("/{camera_id}")
def delete_camera(
    camera_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cam = db.query(Camera).filter(Camera.id == camera_id).first()
    if not cam:
        raise HTTPException(404, "Not found")

    db.delete(cam)
    db.commit()
    return {"message": "deleted"}