from pydantic import BaseModel
from decimal import Decimal


class GroupUserExpenseBase(BaseModel):
    amount: Decimal


class GroupUserExpenseCreate(GroupUserExpenseBase):
    group_user_id: int
    expense_id: int


class GroupUserExpenseResponse(GroupUserExpenseBase):
    id: int
    group_user_id: int
    expense_id: int
    
    class Config:
        from_attributes = True
