from pydantic import BaseModel, ConfigDict
from typing import Optional
class DanhmucDonViBase(BaseModel):
    ten_don_vi: str
 

class DanhmucDonViCreate(DanhmucDonViBase):
    pass
class DanhmucDonViUpdate(BaseModel):
   ten_don_vi: Optional[str] = None

class DanhmucDonViResponse(DanhmucDonViBase):
    id: int

    model_config = ConfigDict(from_attributes=True)