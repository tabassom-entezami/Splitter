#!/usr/bin/env python3

import subprocess
import sys
import os
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
        print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")
    elif status == "error":
        print(f"{Colors.RED}❌ {message}{Colors.ENDC}")
    elif status == "warning":
        print(f"{Colors.YELLOW}⚠️ {message}{Colors.ENDC}")
    elif status == "info":
        print(f"{Colors.BLUE}ℹ️ {message}{Colors.ENDC}")
    else:
        print(f"{message}")

def run_test_script(script_path, description):
    """Run a test script and return success status"""
    print(f"\n{'='*60}")
    print(f"🧪 Running {description}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=False, text=True,
                              cwd=project_root)
        
        if result.returncode == 0:
            print(f"\n✅ {description} - PASSED")
            return True
        else:
            print(f"\n❌ {description} - FAILED")
            return False
            
    except Exception as e:
        print(f"\n❌ {description} - ERROR: {e}")
        return False

def main():
    """Run all test suites"""
    print("🎯 Splitter Complete Test Runner")
    print("This will run all test suites to ensure everything works correctly.")
    
    test_suites = [
        ("tests/test_unit.py", "Unit Tests"),
        ("tests/test_integration.py", "Integration Tests"),
        ("tests/test_docker_integration.py", "Docker Integration Tests"),
    ]
    
    passed = 0
    total = len(test_suites)
    
    for script, description in test_suites:
        script_path = Path(project_root) / script
        if script_path.exists():
            if run_test_script(str(script_path), description):
                passed += 1
        else:
            print(f"\n⚠️ Test script {script} not found, skipping...")
    
    print(f"\n{'='*60}")
    print(f"📊 Final Results: {passed}/{total} test suites passed")
    print('='*60)
    
    if passed == total:
        print("🎉 All tests passed! Your Splitter application is ready!")
        print("\n🚀 Next steps:")
        print("2. Or use Docker: docker compose up -d")
        print("3. Visit API docs: http://localhost:8000/docs")
        return True
    else:
        print("❌ Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
