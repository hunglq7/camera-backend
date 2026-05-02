from models.danh_muc_dien_thoai import DanhMucDienThoai

def create_danh_muc_dien_thoai(db, data):
    record = DanhMucDienThoai(
        ten_thiet_bi=data.ten_thiet_bi,
        loai_thiet_bi=data.loai_thiet_bi,
        thong_so_ky_thuat=data.thong_so_ky_thuat
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_danh_muc_dien_thoai(db, record_id):
    return db.query(DanhMucDienThoai).filter(DanhMucDienThoai.id == record_id).first()

def get_danh_muc_dien_thoais(db):
    return db.query(DanhMucDienThoai).all()

def update_danh_muc_dien_thoai(db, record, data):
    if data.ten_thiet_bi is not None:
        record.ten_thiet_bi = data.ten_thiet_bi
    if data.loai_thiet_bi is not None:
        record.loai_thiet_bi = data.loai_thiet_bi
    if data.thong_so_ky_thuat is not None:
        record.thong_so_ky_thuat = data.thong_so_ky_thuat
    db.commit()
    db.refresh(record)
    return record

def delete_danh_muc_dien_thoai(db, record):
    db.delete(record)
    db.commit()
    return record

def delete_many_danh_muc_dien_thoai(db, ids):
    records = db.query(DanhMucDienThoai).filter(DanhMucDienThoai.id.in_(ids)).all()
    for record in records:
        db.delete(record)
    db.commit()
    return records