from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import List


class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    roles: List[str] = ["user"]


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user_id: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    phone: str | None = None
    avatar: str | None = None
    roles: List[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("roles", mode="before")
    @classmethod
    def split_roles(cls, value):
        if value is None:
            return []
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value
