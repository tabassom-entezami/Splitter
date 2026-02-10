from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from ..core.database import Base


class GroupUser(Base):
    __tablename__ = "group_users"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    deleted_at = Column(DateTime, nullable=True)


    # Relationships
    group = relationship("Group", back_populates="group_users")
    user = relationship("User", back_populates="group_users")
    group_user_expenses = relationship("GroupUserExpense", back_populates="group_user")
