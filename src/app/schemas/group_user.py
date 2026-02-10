from pydantic import BaseModel


class GroupUserBase(BaseModel):
    # Add fields as needed
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
