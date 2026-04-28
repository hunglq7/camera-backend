from datetime import datetime, timezone
from models.camera import Camera
from utils.network import check_camera_status

def create_camera(db, camera_data):
    is_online = check_camera_status(camera_data.ip_address)

    db_camera = Camera(
        name=camera_data.name,
        ip_address=camera_data.ip_address,
        location=camera_data.location,
        is_online=is_online,
        last_check=datetime.now(timezone.utc)
    )

    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    return db_camera


def scan_camera(db, camera):
    camera.is_online = check_camera_status(camera.ip_address)
    camera.last_check = datetime.now(timezone.utc)
    db.commit()
    db.refresh(camera)
    return camera