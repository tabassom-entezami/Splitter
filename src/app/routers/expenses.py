from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..models.expense import Expense
from ..schemas.expense import ExpenseCreate, ExpenseResponse

router = APIRouter(
    prefix="/expenses",
    tags=["expenses"]
)


@router.post("/", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = Expense(
        description=expense.description,
        group_id=expense.group_id,
        created_by_id=expense.created_by_id
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("/", response_model=List[ExpenseResponse])
def read_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    expenses = db.query(Expense).offset(skip).limit(limit).all()
    return expenses


@router.get("/{expense_id}", response_model=ExpenseResponse)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense
