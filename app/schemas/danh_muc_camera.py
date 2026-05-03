from pydantic import BaseModel, ConfigDict
from typing import Optional

class DanhMucCameraBase(BaseModel):
    ten_thiet_bi: str
    thong_so_ky_thuat: str
    hang_san_xuat: str
    nuoc_san_xuat: str

class DanhMucCameraCreate(DanhMucCameraBase):
    pass

class DanhMucCameraUpdate(BaseModel):
    ten_thiet_bi: Optional[str] = None
    thong_so_ky_thuat: Optional[str] = None
    hang_san_xuat: Optional[str] = None
    nuoc_san_xuat: Optional[str] = None

class DanhMucCameraResponse(DanhMucCameraBase):
    id: int

    model_config = ConfigDict(from_attributes=True)