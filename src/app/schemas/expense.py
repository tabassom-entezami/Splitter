from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from .group_user_expense import GroupUserExpenseResponse


class ExpenseBase(BaseModel):
    description: str | None = None


class ExpenseCreate(ExpenseBase):
    group_id: int
    created_by_id: int


class ExpenseResponse(ExpenseBase):
    id: int
    group_id: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    group_user_expenses: List[GroupUserExpenseResponse] = []
    
    class Config:
        from_attributes = True
