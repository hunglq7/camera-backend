from pydantic import BaseModel, ConfigDict
from typing import Optional
class DanhMucDienThoaiBase(BaseModel):
    ten_thiet_bi: str
    loai_thiet_bi: str
    thong_so_ky_thuat: str

class DanhMucDienThoaiCreate(DanhMucDienThoaiBase):
    pass

class DanhMucDienThoaiUpdate(BaseModel):
   ten_thiet_bi: Optional[str] = None
   loai_thiet_bi: Optional[str] = None
   thong_so_ky_thuat: Optional[str] = None

class DanhMucDienThoaiResponse(DanhMucDienThoaiBase):
    id: int

    model_config = ConfigDict(from_attributes=True)