from pydantic import BaseModel, ConfigDict
from typing import Optional


class DanhMucMayXucBase(BaseModel):
    ten_thiet_bi: str
    loai_thiet_bi: str


class DanhMucMayXucCreate(DanhMucMayXucBase):
    pass


class DanhMucMayXucUpdate(BaseModel):
    ten_thiet_bi: Optional[str] = None
    loai_thiet_bi: Optional[str] = None


class DanhMucMayXucResponse(DanhMucMayXucBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
