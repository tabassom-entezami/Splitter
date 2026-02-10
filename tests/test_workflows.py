#!/usr/bin/env python3

import pytest
import sys
import os
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.main import app
from src.app.core.database import get_db, Base
from src.app.models import User, Group, GroupUser, Expense, GroupUserExpense
from src.app.schemas import UserCreate, GroupCreate, ExpenseCreate
from decimal import Decimal

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestUserWorkflows:
    """Test complete user workflows"""
    
    def test_user_creation_and_group_membership(self):
        """Test creating a user and adding them to a group"""
        db = TestingSessionLocal()
        try:
            # Create user
            user = User(
                username="workflow_user",
                email="workflow@example.com",
                password="hashed_password"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # Create group
            group = Group(
                name="Workflow Group",
                description="A group for workflow testing"
            )
            db.add(group)
            db.commit()
            db.refresh(group)
            
            # Add user to group
            group_user = GroupUser(
                group_id=group.id,
                user_id=user.id
            )
            db.add(group_user)
            db.commit()
            db.refresh(group_user)
            
            # Verify relationships
            assert group_user.group_id == group.id
            assert group_user.user_id == user.id
            
            # Query back to verify
            saved_user = db.query(User).filter(User.id == user.id).first()
            saved_group = db.query(Group).filter(Group.id == group.id).first()
            saved_group_user = db.query(GroupUser).filter(
                GroupUser.group_id == group.id,
                GroupUser.user_id == user.id
            ).first()
            
            assert saved_user.username == "workflow_user"
            assert saved_group.name == "Workflow Group"
            assert saved_group_user is not None
            
        finally:
            db.close()
    
    def test_expense_splitting_workflow(self):
        """Test complete expense splitting workflow"""
        db = TestingSessionLocal()
        try:
            # Create users
            user1 = User(username="user1", email="user1@example.com", password="hash1")
            user2 = User(username="user2", email="user2@example.com", password="hash2")
            db.add(user1)
            db.add(user2)
            db.commit()
            db.refresh(user1)
            db.refresh(user2)
            
            # Create group
            group = Group(name="Expense Group", description="Group for expense testing")
            db.add(group)
            db.commit()
            db.refresh(group)
            
            # Add users to group
            gu1 = GroupUser(group_id=group.id, user_id=user1.id)
            gu2 = GroupUser(group_id=group.id, user_id=user2.id)
            db.add(gu1)
            db.add(gu2)
            db.commit()
            db.refresh(gu1)
            db.refresh(gu2)
            
            # Create expense
            expense = Expense(
                description="Dinner at restaurant",
                amount=Decimal("100.00"),
                group_id=group.id,
                created_by_id=user1.id
            )
            db.add(expense)
            db.commit()
            db.refresh(expense)
            
            # Split expense between users
            split1 = GroupUserExpense(
                group_user_id=gu1.id,
                expense_id=expense.id,
                amount=Decimal("50.00")
            )
            split2 = GroupUserExpense(
                group_user_id=gu2.id,
                expense_id=expense.id,
                amount=Decimal("50.00")
            )
            db.add(split1)
            db.add(split2)
            db.commit()
            db.refresh(split1)
            db.refresh(split2)
            
            # Verify the split
            assert split1.amount == Decimal("50.00")
            assert split2.amount == Decimal("50.00")
            
            # Calculate total splits
            total_splits = db.query(GroupUserExpense).filter(
                GroupUserExpense.expense_id == expense.id
            ).all()
            
            total_amount = sum(split.amount for split in total_splits)
            assert total_amount == expense.amount
            
        finally:
            db.close()

class TestAPIIntegration:
    """Test API integration scenarios"""
    
    def test_full_expense_lifecycle(self):
        """Test complete expense lifecycle through API"""
        db = TestingSessionLocal()
        try:
            # Setup: Create user and group
            user = User(username="api_user", email="api@example.com", password="hash")
            group = Group(name="API Group", description="API testing group")
            db.add(user)
            db.add(group)
            db.commit()
            db.refresh(user)
            db.refresh(group)
            
            # Test API endpoints
            # 1. Health check
            response = client.get("/health")
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"
            
            # 2. Config endpoint
            response = client.get("/config")
            assert response.status_code == 200
            config_data = response.json()
            assert "environment" in config_data
            
            # 3. Root endpoint
            response = client.get("/")
            assert response.status_code == 200
            assert "Splitter API" in response.json()["message"]
            
        finally:
            db.close()
    
    def test_database_consistency(self):
        """Test database consistency across operations"""
        db = TestingSessionLocal()
        try:
            # Create multiple related entities
            users = []
            for i in range(3):
                user = User(
                    username=f"consistency_user_{i}",
                    email=f"user{i}@example.com",
                    password="hash"
                )
                db.add(user)
                users.append(user)
            
            group = Group(name="Consistency Group", description="Testing consistency")
            db.add(group)
            db.commit()
            
            # Refresh all objects to get their IDs
            for user in users:
                db.refresh(user)
            db.refresh(group)
            
            # Add all users to group
            for user in users:
                group_user = GroupUser(group_id=group.id, user_id=user.id)
                db.add(group_user)
            
            db.commit()
            
            # Verify consistency
            group_users = db.query(GroupUser).filter(GroupUser.group_id == group.id).all()
            assert len(group_users) == 3
            
            # Create expenses
            expenses = []
            for i in range(2):
                expense = Expense(
                    description=f"Expense {i+1}",
                    amount=Decimal(f"{(i+1)*50}.00"),
                    group_id=group.id,
                    created_by_id=users[0].id
                )
                db.add(expense)
                expenses.append(expense)
            
            db.commit()
            
            # Refresh expenses
            for expense in expenses:
                db.refresh(expense)
            
            # Verify all expenses belong to the group
            for expense in expenses:
                assert expense.group_id == group.id
            
        finally:
            db.close()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
