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

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
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

class TestAPI:
    """Test API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Splitter API" in data["message"]
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
    
    def test_hello_endpoint(self):
        """Test hello endpoint"""
        response = client.get("/hello/testuser")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hello testuser"
    
    def test_config_endpoint(self):
        """Test config endpoint"""
        response = client.get("/config")
        assert response.status_code == 200
        data = response.json()
        assert "database_url" in data
        assert "environment" in data
    
    def test_items_endpoint(self):
        """Test items endpoint"""
        response = client.get("/items/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10  # Default limit

class TestDatabaseModels:
    """Test database models"""
    
    def test_user_model(self):
        """Test User model creation"""
        db = TestingSessionLocal()
        try:
            user = User(
                username="testuser",
                email="test@example.com",
                password="hashed_password"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            assert user.id is not None
            assert user.username == "testuser"
            assert user.email == "test@example.com"
            assert user.password == "hashed_password"
        finally:
            db.close()
    
    def test_group_model(self):
        """Test Group model creation"""
        db = TestingSessionLocal()
        try:
            group = Group(
                name="Test Group",
                description="A test group for testing"
            )
            db.add(group)
            db.commit()
            db.refresh(group)
            
            assert group.id is not None
            assert group.name == "Test Group"
            assert group.description == "A test group for testing"
        finally:
            db.close()
    
    def test_expense_model(self):
        """Test Expense model creation"""
        db = TestingSessionLocal()
        try:
            # Create a user and group first
            user = User(username="testuser", email="test@example.com", password="hashed")
            group = Group(name="Test Group", description="Test")
            db.add(user)
            db.add(group)
            db.commit()
            db.refresh(user)
            db.refresh(group)
            
            # Create expense
            expense = Expense(
                description="Test Expense",
                amount=100.50,
                group_id=group.id,
                created_by_id=user.id
            )
            db.add(expense)
            db.commit()
            db.refresh(expense)
            
            assert expense.id is not None
            assert expense.description == "Test Expense"
            assert expense.amount == 100.50
            assert expense.group_id == group.id
            assert expense.created_by_id == user.id
        finally:
            db.close()

class TestSchemas:
    """Test Pydantic schemas"""
    
    def test_user_schemas(self):
        """Test user schemas"""
        from src.app.schemas import UserCreate, UserResponse
        from datetime import datetime
        
        # Test UserCreate
        user_create = UserCreate(
            username="testuser",
            email="test@example.com",
            password="secret123"
        )
        assert user_create.username == "testuser"
        assert user_create.email == "test@example.com"
        assert user_create.password == "secret123"
        
        # Test UserResponse
        user_response = UserResponse(
            id=1,
            username="testuser",
            email="test@example.com",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert user_response.id == 1
        assert user_response.username == "testuser"
    
    def test_group_schemas(self):
        """Test group schemas"""
        from src.app.schemas import GroupCreate, GroupResponse
        from datetime import datetime
        
        # Test GroupCreate
        group_create = GroupCreate(
            name="Test Group",
            description="A test group"
        )
        assert group_create.name == "Test Group"
        assert group_create.description == "A test group"
        
        # Test GroupResponse
        group_response = GroupResponse(
            id=1,
            name="Test Group",
            description="A test group",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert group_response.id == 1
        assert group_response.name == "Test Group"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
