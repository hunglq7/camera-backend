from models.danh_muc_may_cao import DanhMucMayCao

def create_danh_muc_may_cao(db, data):
    record = DanhMucMayCao(
        ten_thiet_bi=data.ten_thiet_bi,
        loai_thiet_bi=data.loai_thiet_bi,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_danh_muc_may_cao(db, record_id):
    return db.query(DanhMucMayCao).filter(DanhMucMayCao.id == record_id).first()

def get_danh_muc_may_caos(db):
    return db.query(DanhMucMayCao).all()

def update_danh_muc_may_cao(db, record, data):
    if data.ten_thiet_bi is not None:
        record.ten_thiet_bi = data.ten_thiet_bi
    if data.loai_thiet_bi is not None:
        record.loai_thiet_bi = data.loai_thiet_bi
    db.commit()
    db.refresh(record)
    return record

def delete_danh_muc_may_cao(db, record):
    db.delete(record)
    db.commit()
    return record

def delete_many_danh_muc_may_cao(db, ids):
    records = db.query(DanhMucMayCao).filter(DanhMucMayCao.id.in_(ids)).all()
    for record in records:
        db.delete(record)
    db.commit()
    return records