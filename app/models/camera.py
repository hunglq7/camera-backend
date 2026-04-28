from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone
from core.database import Base

class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    ip_address = Column(String(50), nullable=False)
    location = Column(String(200))
    is_online = Column(Boolean, default=False)
    last_check = Column(DateTime, default=lambda: datetime.now(timezone.utc))