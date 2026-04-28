from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class TongHopCameraBase(BaseModel):
    camera_id: int
    total_scans: Optional[int] = 0
    summary: Optional[str] = None


class TongHopCameraCreate(TongHopCameraBase):
    pass


class TongHopCameraUpdate(BaseModel):
    total_scans: Optional[int] = None
    summary: Optional[str] = None


class TongHopCameraResponse(TongHopCameraBase):
    id: int
    last_updated: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
