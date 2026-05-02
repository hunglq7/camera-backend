from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import io

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.camera import Camera
from schemas.camera import CameraCreate, CameraResponse
from services.camera_service import (
    create_camera,
    scan_camera,
    update_camera,
    import_cameras_from_excel,
    build_camera_template,
)

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


@router.post("/import")
async def import_cameras(
    upload_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if upload_file.content_type not in (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel",
    ):
        raise HTTPException(400, "Please upload an Excel file")

    data = await upload_file.read()
    try:
        created, updated = import_cameras_from_excel(db, data)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    return {"created": created, "updated": updated}


@router.get("/template")
def get_camera_template(
    current_user: User = Depends(get_current_user)
):
    template_bytes = build_camera_template()
    return StreamingResponse(
        io.BytesIO(template_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=camera_template.xlsx"},
    )


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


@router.put("/{camera_id}", response_model=CameraResponse)
def update_camera_endpoint(
    camera_id: int,
    camera: CameraCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cam = db.query(Camera).filter(Camera.id == camera_id).first()
    if not cam:
        raise HTTPException(404, "Not found")

    return update_camera(db, cam, camera)


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


@router.delete("/")
def delete_multiple_cameras(
    ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cameras = db.query(Camera).filter(Camera.id.in_(ids)).all()
    for cam in cameras:
        db.delete(cam)
    db.commit()
    return {"message": "deleted"}