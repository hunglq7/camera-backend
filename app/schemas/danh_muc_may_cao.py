from pydantic import BaseModel, ConfigDict
from typing import Optional

class DanhMucMayCaoBase(BaseModel):
    ten_thiet_bi: str
    loai_thiet_bi: str

class DanhMucMayCaoCreate(DanhMucMayCaoBase):
    pass

class DanhMucMayCaoUpdate(BaseModel):
    ten_thiet_bi: Optional[str] = None
    loai_thiet_bi: Optional[str] = None

class DanhMucMayCaoResponse(DanhMucMayCaoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)