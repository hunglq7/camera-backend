from sqlalchemy import Column, Integer, String
from core.database import Base
class DanhmucDonVi(Base):
    __tablename__ = "danh_muc_don_vi"

    id = Column(Integer, primary_key=True, index=True)
    ten_don_vi = Column(String(100), nullable=False)