from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.security import get_current_user
from models.user import User
from schemas.vi_tri_lap_dat import (
    ViTriLapDatCreate,
    ViTriLapDatUpdate,
    ViTriLapDatResponse,
)
from services.vi_tri_lap_dat_service import (
    create_vi_tri_lap_dat,
    get_vi_tri_lap_dat,
    get_vi_tri_lap_dats,
    update_vi_tri_lap_dat,
    delete_vi_tri_lap_dat,
    delete_many_vi_tri_lap_dat,
)

router = APIRouter(prefix="/vi-tri-lap-dat", tags=["Vi Tri Lap Dat"])

@router.post("/", response_model=ViTriLapDatResponse, status_code=status.HTTP_201_CREATED)
def add_vi_tri_lap_dat(
    payload: ViTriLapDatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_vi_tri_lap_dat(db, payload)

@router.get("/", response_model=List[ViTriLapDatResponse])
def list_vi_tri_lap_dat(db: Session = Depends(get_db)):
    return get_vi_tri_lap_dats(db)

@router.get("/{record_id}", response_model=ViTriLapDatResponse)
def read_vi_tri_lap_dat(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_vi_tri_lap_dat(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return record

@router.put("/{record_id}", response_model=ViTriLapDatResponse)
def update_vi_tri_lap_dat_endpoint(
    record_id: int,
    payload: ViTriLapDatUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_vi_tri_lap_dat(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return update_vi_tri_lap_dat(db, record, payload)

@router.delete("/{record_id}")
def delete_vi_tri_lap_dat_endpoint(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_vi_tri_lap_dat(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    delete_vi_tri_lap_dat(db, record)
    return {"message": "deleted"}

@router.delete("/")
def delete_many_vi_tri_lap_dat_endpoint(
    ids: List[int] = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_many_vi_tri_lap_dat(db, ids)
    return {"deleted_count": len(deleted)}