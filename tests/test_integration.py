#!/usr/bin/env python3

import pytest
import sys
import os
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.app.core.config import settings
from src.app.core.database import engine, Base
from src.app.models import User, Group, GroupUser, Expense, GroupUserExpense
from src.app.schemas import UserCreate, GroupCreate, ExpenseCreate

class TestConfiguration:
    """Test application configuration"""
    
    def test_settings_instance(self):
        """Test that settings can be instantiated"""
        assert settings is not None
        assert hasattr(settings, 'database_url')
        assert hasattr(settings, 'environment')
    
    def test_database_url(self):
        """Test database URL configuration"""
        assert settings.database_url is not None
        assert isinstance(settings.database_url, str)
        # Should contain postgresql for production or sqlite for testing
        assert "postgresql" in settings.database_url or "sqlite" in settings.database_url
    
    def test_environment_setting(self):
        """Test environment configuration"""
        assert settings.environment in ["development", "testing", "production"]

class TestDatabaseConnection:
    """Test database connectivity and setup"""
    
    def test_engine_creation(self):
        """Test that database engine can be created"""
        assert engine is not None
    
    def test_base_metadata(self):
        """Test that Base metadata is properly configured"""
        assert Base is not None
        assert hasattr(Base, 'metadata')
        assert len(Base.metadata.tables) > 0
    
    def test_table_creation(self):
        """Test that all model tables are registered"""
        tables = Base.metadata.tables.keys()
        expected_tables = ['users', 'groups', 'group_users', 'expenses', 'group_user_expenses']
        
        for table in expected_tables:
            assert table in tables, f"Table {table} not found in metadata"

class TestModelRelationships:
    """Test model relationships and constraints"""
    
    def test_user_relationships(self):
        """Test User model relationships"""
        # Check that User model has the expected relationships
        user_columns = [col.name for col in User.__table__.columns]
        expected_columns = ['id', 'username', 'email', 'password', 'created_at', 'updated_at']
        
        for col in expected_columns:
            assert col in user_columns, f"Column {col} not found in User model"
    
    def test_group_relationships(self):
        """Test Group model relationships"""
        group_columns = [col.name for col in Group.__table__.columns]
        expected_columns = ['id', 'name', 'description', 'created_at', 'updated_at']
        
        for col in expected_columns:
            assert col in group_columns, f"Column {col} not found in Group model"
    
    def test_expense_relationships(self):
        """Test Expense model relationships"""
        expense_columns = [col.name for col in Expense.__table__.columns]
        expected_columns = ['id', 'description', 'amount', 'group_id', 'created_by_id', 'created_at', 'updated_at']
        
        for col in expected_columns:
            assert col in expense_columns, f"Column {col} not found in Expense model"

class TestSchemaValidation:
    """Test Pydantic schema validation"""
    
    def test_user_create_validation(self):
        """Test UserCreate schema validation"""
        # Valid data
        valid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123"
        }
        user = UserCreate(**valid_data)
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password == "securepassword123"
        
        # Invalid email
        invalid_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "securepassword123"
        }
        with pytest.raises(ValueError):
            UserCreate(**invalid_data)
    
    def test_group_create_validation(self):
        """Test GroupCreate schema validation"""
        valid_data = {
            "name": "Test Group",
            "description": "A test group"
        }
        group = GroupCreate(**valid_data)
        assert group.name == "Test Group"
        assert group.description == "A test group"
        
        # Missing required field
        invalid_data = {
            "description": "A test group"
        }
        with pytest.raises(ValueError):
            GroupCreate(**invalid_data)
    
    def test_expense_create_validation(self):
        """Test ExpenseCreate schema validation"""
        valid_data = {
            "description": "Test Expense",
            "amount": 100.50,
            "group_id": 1,
            "created_by_id": 1
        }
        expense = ExpenseCreate(**valid_data)
        assert expense.description == "Test Expense"
        assert expense.amount == 100.50
        assert expense.group_id == 1
        assert expense.created_by_id == 1
        
        # Negative amount should fail
        invalid_data = {
            "description": "Test Expense",
            "amount": -50.0,
            "group_id": 1,
            "created_by_id": 1
        }
        with pytest.raises(ValueError):
            ExpenseCreate(**invalid_data)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
