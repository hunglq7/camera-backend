from sqlalchemy import Column, Integer, String
from core.database import Base

class ViTriLapDat(Base):
    __tablename__ = "vi_tri_lap_dat"

    id = Column(Integer, primary_key=True, index=True)
    ten_vi_tri = Column(String(255), nullable=False)
    mo_ta = Column(String(500), nullable=True)