from models.danh_muc_don_vi import DanhmucDonVi

def create_danh_muc_don_vi(db, data):
    record = DanhmucDonVi(
        ten_don_vi=data.ten_don_vi
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_danh_muc_don_vi(db, record_id):
    return db.query(DanhmucDonVi).filter(DanhmucDonVi.id == record_id).first()
    
 
def get_danh_muc_don_vis(db):
    return db.query(DanhmucDonVi).all()

def update_danh_muc_don_vi(db, record, data):
    if data.ten_don_vi is not None:
        record.ten_don_vi = data.ten_don_vi
    db.commit()
    db.refresh(record)
    return record

def delete_danh_muc_don_vi(db, record):
    db.delete(record)
    db.commit()
    return record

def delete_many_danh_muc_don_vi(db, ids):
    records = db.query(DanhmucDonVi).filter(DanhmucDonVi.id.in_(ids)).all()
    for record in records:
        db.delete(record)
    db.commit()
    return records