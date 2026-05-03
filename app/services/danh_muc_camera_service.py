from models.danh_muc_camera import DanhMucCamera

def create_danh_muc_camera(db, data):
    record = DanhMucCamera(
        ten_thiet_bi=data.ten_thiet_bi,
        thong_so_ky_thuat=data.thong_so_ky_thuat,
        hang_san_xuat=data.hang_san_xuat,
        nuoc_san_xuat=data.nuoc_san_xuat
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_danh_muc_camera(db, record_id):
    return db.query(DanhMucCamera).filter(DanhMucCamera.id == record_id).first()

def get_danh_muc_cameras(db):
    return db.query(DanhMucCamera).all()

def update_danh_muc_camera(db, record, data):
    if data.ten_thiet_bi is not None:
        record.ten_thiet_bi = data.ten_thiet_bi
    if data.thong_so_ky_thuat is not None:
        record.thong_so_ky_thuat = data.thong_so_ky_thuat
    if data.hang_san_xuat is not None:
        record.hang_san_xuat = data.hang_san_xuat
    if data.nuoc_san_xuat is not None:
        record.nuoc_san_xuat = data.nuoc_san_xuat
    db.commit()
    db.refresh(record)
    return record

def delete_danh_muc_camera(db, record):
    db.delete(record)
    db.commit()
    return record

def delete_many_danh_muc_camera(db, ids):
    records = db.query(DanhMucCamera).filter(DanhMucCamera.id.in_(ids)).all()
    for record in records:
        db.delete(record)
    db.commit()
    return records