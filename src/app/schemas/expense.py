from pydantic import BaseModel
from datetime import datetime



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
    
    class Config:
        from_attributes = True
