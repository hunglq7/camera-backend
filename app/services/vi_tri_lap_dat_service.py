from models.vi_tri_lap_dat import ViTriLapDat

def create_vi_tri_lap_dat(db, data):
    record = ViTriLapDat(
        ten_vi_tri=data.ten_vi_tri,
        mo_ta=data.mo_ta
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_vi_tri_lap_dat(db, record_id):
    return db.query(ViTriLapDat).filter(ViTriLapDat.id == record_id).first()

def get_vi_tri_lap_dats(db):
    return db.query(ViTriLapDat).all()

def update_vi_tri_lap_dat(db, record, data):
    if data.ten_vi_tri is not None:
        record.ten_vi_tri = data.ten_vi_tri
    if data.mo_ta is not None:
        record.mo_ta = data.mo_ta
    db.commit()
    db.refresh(record)
    return record

def delete_vi_tri_lap_dat(db, record):
    db.delete(record)
    db.commit()
    return record

def delete_many_vi_tri_lap_dat(db, ids):
    records = db.query(ViTriLapDat).filter(ViTriLapDat.id.in_(ids)).all()
    for record in records:
        db.delete(record)
    db.commit()
    return records