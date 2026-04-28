from datetime import datetime, timezone
from models.tong_hop_camera import TongHopCamera
from models.camera import Camera


def create_tong_hop_camera(db, data):
    camera = db.query(Camera).filter(Camera.id == data.camera_id).first()
    if not camera:
        raise ValueError("Camera not found")

    record = TongHopCamera(
        camera_id=data.camera_id,
        total_scans=data.total_scans or 0,
        summary=data.summary,
        last_updated=datetime.now(timezone.utc)
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_tong_hop_camera(db, record_id):
    return db.query(TongHopCamera).filter(TongHopCamera.id == record_id).first()


def get_tong_hop_cameras(db):
    return db.query(TongHopCamera).all()


def update_tong_hop_camera(db, record, data):
    if data.total_scans is not None:
        record.total_scans = data.total_scans
    if data.summary is not None:
        record.summary = data.summary
    record.last_updated = datetime.now(timezone.utc)
    db.commit()
    db.refresh(record)
    return record


def delete_tong_hop_camera(db, record):
    db.delete(record)
    db.commit()
    return record
