from pydantic import BaseModel
from datetime import datetime


class GroupUserBase(BaseModel):
    pass


class GroupUserCreate(GroupUserBase):
    group_id: int
    user_id: int


class GroupUserResponse(GroupUserBase):
    id: int
    group_id: int
    user_id: int
    
    class Config:
        from_attributes = True
