from pydantic import BaseModel


class GroupUserExpenseBase(BaseModel):
    # Add fields as needed
    pass


class GroupUserExpenseCreate(GroupUserExpenseBase):
    group_user_id: int
    expense_id: int


class GroupUserExpenseResponse(GroupUserExpenseBase):
    id: int
    group_user_id: int
    expense_id: int
    
    class Config:
        from_attributes = True
