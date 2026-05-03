from pydantic import BaseModel, ConfigDict
from typing import Optional

class ViTriLapDatBase(BaseModel):
    ten_vi_tri: str
    mo_ta: Optional[str] = None

class ViTriLapDatCreate(ViTriLapDatBase):
    pass

class ViTriLapDatUpdate(BaseModel):
    ten_vi_tri: Optional[str] = None
    mo_ta: Optional[str] = None

class ViTriLapDatResponse(ViTriLapDatBase):
    id: int

    model_config = ConfigDict(from_attributes=True)