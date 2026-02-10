#!/usr/bin/env python3

import pytest
import sys
import os
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def run_all_tests():
    """Run all test suites"""
    print("🧪 Running Complete Splitter Test Suite")
    print("=" * 60)
    
    test_files = [
        ("test_unit.py", "Unit Tests"),
        ("test_api.py", "API Tests"),
        ("test_integration.py", "Integration Tests"),
        ("test_workflows.py", "Workflow Tests"),
        ("test_docker_integration.py", "Docker Integration Tests")
    ]
    
    passed = 0
    total = len(test_files)
    
    for test_file, description in test_files:
        print(f"\n📋 Running {description} ({test_file})")
        print("-" * 40)
        
        test_path = os.path.join(os.path.dirname(__file__), test_file)
        
        if os.path.exists(test_path):
            try:
                # Run pytest for the test file
                exit_code = pytest.main([test_path, "-v", "--tb=short"])
                
                if exit_code == 0:
                    print(f"✅ {description} - PASSED")
                    passed += 1
                else:
                    print(f"❌ {description} - FAILED")
            except Exception as e:
                print(f"❌ {description} - ERROR: {e}")
        else:
            print(f"⚠️ {test_file} not found, skipping...")
    
    print("\n" + "=" * 60)
    print(f"📊 Final Results: {passed}/{total} test suites passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All tests passed! Your Splitter application is ready!")
        print("\n🚀 Next steps:")
        print("1. Create .env file from .env.example")
        print("2. Start development: python -m uvicorn src.app.main:app --reload")
        print("3. Or use Docker: docker compose up -d")
        print("4. Visit API docs: http://localhost:8000/docs")
        return True
    else:
        print("❌ Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
