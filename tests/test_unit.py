#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_status(message, status="info"):
    if status == "success":
        print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")
    elif status == "error":
        print(f"{Colors.RED}❌ {message}{Colors.ENDC}")
    elif status == "warning":
        print(f"{Colors.YELLOW}⚠️ {message}{Colors.ENDC}")
    elif status == "info":
        print(f"{Colors.BLUE}ℹ️ {message}{Colors.ENDC}")
    else:
        print(f"{message}")

def test_imports():
    """Test all imports work correctly"""
    print_status("Testing imports...", "info")
    
    try:
        # Test SQLAlchemy
        from sqlalchemy import create_engine
        print_status("SQLAlchemy imported", "success")
        
        # Test Alembic context
        from alembic import context
        print_status("Alembic context imported", "success")
        
        # Test our models
        from src.app.core.database import Base
        from src.app.models import *
        print_status("All models imported", "success")
        
        # Test Pydantic
        from pydantic import BaseModel
        print_status("Pydantic imported", "success")
        
        print_status("All imports successful!", "success")
        return True
        
    except ImportError as e:
        print_status(f"Import error: {e}", "error")
        print_status("Please install dependencies: pip install -e .", "warning")
        return False
    except Exception as e:
        print_status(f"Error: {e}", "error")
        return False

def test_alembic_configuration():
    """Test Alembic configuration"""
    print_status("Testing Alembic configuration...", "info")
    
    try:
        # Test alembic context import
        from alembic import context
        print_status("Alembic context imported successfully", "success")
        
        # Test our database setup
        from src.app.core.database import Base
        from src.app.models import *
        
        print_status(f"Database metadata loaded with {len(Base.metadata.tables)} tables:", "success")
        for table_name in Base.metadata.tables.keys():
            print_status(f"  - {table_name}", "info")
        
        print_status("Alembic configuration test passed!", "success")
        return True
        
    except ImportError as e:
        print_status(f"Import error: {e}", "error")
        print_status("This usually means dependencies are not installed.", "warning")
        print_status("Run: pip install -e .", "warning")
        return False
    except Exception as e:
        print_status(f"Error: {e}", "error")
        import traceback
        traceback.print_exc()
        return False

def test_models():
    """Test model definitions"""
    print_status("Testing models...", "info")
    
    try:
        from src.app.models import User, Group, GroupUser, Expense, GroupUserExpense
        
        # Test User model
        user = User(username="testuser", email="test@example.com", password="hashed")
        print_status("User model works", "success")
        
        # Test Group model
        group = Group(name="Test Group", description="A test group")
        print_status("Group model works", "success")
        
        # Test Expense model
        expense = Expense(description="Test expense", group_id=1, created_by_id=1)
        print_status("Expense model works", "success")
        
        # Test GroupUser model
        group_user = GroupUser(group_id=1, user_id=1)
        print_status("GroupUser model works", "success")
        
        # Test GroupUserExpense model
        from decimal import Decimal
        group_user_expense = GroupUserExpense(group_user_id=1, expense_id=1, amount=Decimal("10.50"))
        print_status("GroupUserExpense model works", "success")
        
        return True
        
    except Exception as e:
        print_status(f"Model test failed: {e}", "error")
        return False

def test_schemas():
    """Test Pydantic schemas"""
    print_status("Testing schemas...", "info")
    
    try:
        from src.app.schemas import UserCreate, GroupCreate, ExpenseCreate, UserResponse, GroupResponse, ExpenseResponse
        from datetime import datetime
        
        # Test user schemas
        user_create = UserCreate(username="testuser", email="test@example.com", password="secret")
        user_response = UserResponse(id=1, username="testuser", email="test@example.com", created_at=datetime.now(), updated_at=datetime.now())
        print_status("User schemas work", "success")
        
        # Test group schemas
        group_create = GroupCreate(name="Test Group", description="A test group")
        group_response = GroupResponse(id=1, name="Test Group", description="A test group", created_at=datetime.now(), updated_at=datetime.now())
        print_status("Group schemas work", "success")
        
        # Test expense schemas
        expense_create = ExpenseCreate(group_id=1, created_by_id=1, description="Test expense")
        expense_response = ExpenseResponse(id=1, group_id=1, created_by_id=1, description="Test expense", created_at=datetime.now(), updated_at=datetime.now())
        print_status("Expense schemas work", "success")
        
        return True
        
    except Exception as e:
        print_status(f"Schema test failed: {e}", "error")
        return False

def test_fastapi_app():
    """Test FastAPI application"""
    print_status("Testing FastAPI app...", "info")
    
    try:
        from src.app.main import app
        
        # Test app configuration
        assert app.title == "Splitter API"
        assert app.version == "1.0.0"
        print_status("FastAPI app configured correctly", "success")
        
        # Test routes
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/health", "/hello/{name}", "/config", "/items/"]
        
        missing_routes = []
        for route in expected_routes:
            if route in routes:
                print_status(f"Route {route} exists", "success")
            else:
                missing_routes.append(route)
        
        if missing_routes:
            print_status(f"Missing routes: {missing_routes}", "error")
            return False
        
        return True
        
    except Exception as e:
        print_status(f"FastAPI test failed: {e}", "error")
        return False

def run_unit_tests():
    """Run all unit tests"""
    print(f"{Colors.BOLD}{Colors.BLUE}🧪 Splitter Unit Test Suite{Colors.ENDC}")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Alembic Configuration", test_alembic_configuration),
        ("Model Tests", test_models),
        ("Schema Tests", test_schemas),
        ("FastAPI App Tests", test_fastapi_app),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{Colors.BOLD}📋 {test_name}{Colors.ENDC}")
        print("-" * 30)
        
        if test_func():
            passed += 1
            print_status(f"{test_name} PASSED", "success")
        else:
            print_status(f"{test_name} FAILED", "error")
    
    print("\n" + "=" * 50)
    print(f"{Colors.BOLD}📊 Unit Test Results: {passed}/{total} tests passed{Colors.ENDC}")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 All unit tests passed!{Colors.ENDC}")
        return True
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ Some unit tests failed.{Colors.ENDC}")
        return False

if __name__ == "__main__":
    success = run_unit_tests()
    sys.exit(0 if success else 1)
