from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CameraBase(BaseModel):
    name: str
    ip_address: str
    location: Optional[str] = None

class CameraCreate(CameraBase):
    pass

class CameraResponse(CameraBase):
    id: int
    is_online: bool
    last_check: datetime

    model_config = ConfigDict(from_attributes=True)