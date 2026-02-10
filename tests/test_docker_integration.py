#!/usr/bin/env python3

import subprocess
import time
import requests
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

def run_command(command, description, timeout=30):
    """Run a command and return success status"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout, cwd=project_root)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True, result.stdout
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT")
        return False, "Command timed out"
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False, str(e)

def test_docker_setup():
    """Test complete Docker setup"""
    print("🐳 Docker Integration Test Suite")
    print("=" * 50)
    
    # Test 1: Check Docker and Docker Compose
    print("\n📋 Checking Docker installation...")
    success, _ = run_command("docker --version", "Docker version check")
    if not success:
        return False
    
    success, _ = run_command("docker compose version", "Docker Compose version check")
    if not success:
        return False
    
    # Test 2: Build Docker image
    print("\n🏗️ Building Docker image...")
    success, _ = run_command("docker build -t splitter-test .", "Docker build", timeout=120)
    if not success:
        return False
    
    # Test 3: Validate Docker Compose configuration
    print("\n📝 Validating Docker Compose configuration...")
    success, _ = run_command("docker compose config", "Docker Compose config validation")
    if not success:
        return False
    
    # Test 4: Start services
    print("\n🚀 Starting Docker services...")
    success, _ = run_command("docker compose up -d", "Starting services", timeout=60)
    if not success:
        return False
    
    # Wait for services to be ready
    print("⏳ Waiting for services to be ready...")
    time.sleep(10)
    
    # Test 5: Check service health
    print("\n🏥 Checking service health...")
    
    # Check database health
    for i in range(30):  # Wait up to 30 seconds
        success, _ = run_command("docker compose exec -T db pg_isready -U postgres", "Database health check")
        if success:
            break
        time.sleep(1)
    
    if not success:
        print("❌ Database not ready after 30 seconds")
        run_command("docker compose down", "Cleaning up services")
        return False
    
    # Test 6: Check API health
    print("\n🌐 Checking API health...")
    for i in range(30):  # Wait up to 30 seconds
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ API health check - SUCCESS")
                break
        except:
            pass
        time.sleep(1)
    else:
        print("❌ API not ready after 30 seconds")
        run_command("docker compose down", "Cleaning up services")
        return False
    
    # Test 7: Test API endpoints
    print("\n🔍 Testing API endpoints...")
    
    try:
        # Test root endpoint
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint - SUCCESS")
        else:
            print(f"❌ Root endpoint - FAILED: {response.status_code}")
        
        # Test hello endpoint
        response = requests.get("http://localhost:8000/hello/docker", timeout=5)
        if response.status_code == 200:
            print("✅ Hello endpoint - SUCCESS")
        else:
            print(f"❌ Hello endpoint - FAILED: {response.status_code}")
        
        # Test config endpoint
        response = requests.get("http://localhost:8000/config", timeout=5)
        if response.status_code == 200:
            print("✅ Config endpoint - SUCCESS")
        else:
            print(f"❌ Config endpoint - FAILED: {response.status_code}")
            
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
    
    # Test 8: Check logs
    print("\n📋 Checking service logs...")
    success, logs = run_command("docker compose logs --tail=10 web", "Web service logs")
    if success:
        print("Recent web logs:")
        print(logs[-500:])  # Show last 500 characters
    
    # Cleanup
    print("\n🧹 Cleaning up...")
    run_command("docker compose down", "Stopping services")
    
    print("\n🎉 Docker integration test completed successfully!")
    return True

if __name__ == "__main__":
    try:
        success = test_docker_setup()
        if success:
            print("\n✅ All Docker integration tests passed!")
            print("🚀 You can now run: docker compose up -d")
            sys.exit(0)
        else:
            print("\n❌ Docker integration tests failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        run_command("docker compose down", "Cleaning up services")
        sys.exit(1)
