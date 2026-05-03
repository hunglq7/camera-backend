from sqlalchemy import Column, Integer, String
from core.database import Base

class DanhMucCamera(Base):
    __tablename__ = "danh_muc_camera"

    id = Column(Integer, primary_key=True, index=True)
    ten_thiet_bi = Column(String(255), nullable=False)
    thong_so_ky_thuat = Column(String(255), nullable=False)
    hang_san_xuat = Column(String(255), nullable=False)
    nuoc_san_xuat = Column(String(255), nullable=False)