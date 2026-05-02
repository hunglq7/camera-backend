from sqlalchemy import Column, Integer, String
from core.database import Base
class DanhMucDienThoai(Base):
    __tablename__ = "danh_muc_dien_thoai"

    id = Column(Integer, primary_key=True, index=True)
    ten_thiet_bi = Column(String(100), nullable=False)  
    loai_thiet_bi = Column(String(100), nullable=False)
    thong_so_ky_thuat = Column(String(255), nullable=False)