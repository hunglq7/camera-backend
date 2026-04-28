from sqlalchemy import Column, Integer, String
from core.database import Base

class DanhMucMayCao(Base):
    __tablename__ = "danh_muc_may_cao"

    id = Column(Integer, primary_key=True, index=True)
    ten_thiet_bi = Column(String(100), nullable=False)
    loai_thiet_bi = Column(String(100), nullable=False)