from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(12),  index=True)
    avatar = Column(String(255), nullable=True)  # Avatar file path
    hashed_password = Column(String(255), nullable=False)
    roles = Column(String(255), nullable=True, default="user")  # Comma-separated roles
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
