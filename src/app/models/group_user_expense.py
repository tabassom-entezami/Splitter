from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship

from ..core.database import Base


class GroupUserExpense(Base):
    __tablename__ = "group_user_expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    group_user_id = Column(Integer, ForeignKey("group_users.id"), nullable=False)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False)
    amount = Column(Numeric, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    deleted_at = Column(DateTime, nullable=True)



    
    # Relationships
    group_user = relationship("GroupUser", back_populates="group_user_expenses")
    expense = relationship("Expense", back_populates="group_user_expenses")
