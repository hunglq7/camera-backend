from typing import List, Optional, Any, Dict
from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import datetime

from .auth import UserResponse


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    password: Optional[str] = None
    roles: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='before')
    @classmethod
    def validate_partial_update(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        # Convert empty strings to None for optional fields
        result = {}
        for k, v in values.items():
            if k in ['username', 'email', 'phone', 'avatar', 'password'] and v == "":
                result[k] = None
            elif k == 'roles' and v == []:
                result[k] = None
            else:
                result[k] = v
        return result


class BulkDeleteRequest(BaseModel):
    ids: List[int]


class UserListResponse(BaseModel):
    list: List[UserResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)
