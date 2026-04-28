from models.danh_muc_may_xuc import DanhMucMayXuc


def create_danh_muc_may_xuc(db, data):
    record = DanhMucMayXuc(
        ten_thiet_bi=data.ten_thiet_bi,
        loai_thiet_bi=data.loai_thiet_bi,
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_danh_muc_may_xuc(db, record_id):
    return db.query(DanhMucMayXuc).filter(DanhMucMayXuc.id == record_id).first()


def get_danh_muc_may_xucs(db):
    return db.query(DanhMucMayXuc).all()


def update_danh_muc_may_xuc(db, record, data):
    if data.ten_thiet_bi is not None:
        record.ten_thiet_bi = data.ten_thiet_bi
    if data.loai_thiet_bi is not None:
        record.loai_thiet_bi = data.loai_thiet_bi

    db.commit()
    db.refresh(record)
    return record


def delete_danh_muc_may_xuc(db, record):
    db.delete(record)
    db.commit()
    return record


def delete_many_danh_muc_may_xuc(db, ids):
    records = db.query(DanhMucMayXuc).filter(DanhMucMayXuc.id.in_(ids)).all()
    for record in records:
        db.delete(record)
    db.commit()
    return records
