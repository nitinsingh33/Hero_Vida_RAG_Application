#!/usr/bin/env python3
"""
Setup script for Hero Vida RAG Application
This script helps automate the setup process for the application.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, cwd=None, shell=False):
    """Run a shell command and return the result"""
    try:
        if shell or platform.system() == "Windows":
            result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        else:
            result = subprocess.run(command.split(), cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_requirements():
    """Check if required software is installed"""
    print("🔍 Checking requirements...")
    
    # Check Python
    success, stdout, stderr = run_command("python --version")
    if success:
        print(f"✅ Python: {stdout.strip()}")
    else:
        print("❌ Python not found. Please install Python 3.8+")
        return False
    
    # Check Node.js
    success, stdout, stderr = run_command("node --version")
    if success:
        print(f"✅ Node.js: {stdout.strip()}")
    else:
        print("❌ Node.js not found. Please install Node.js 16+")
        return False
    
    # Check npm
    success, stdout, stderr = run_command("npm --version")
    if success:
        print(f"✅ npm: {stdout.strip()}")
    else:
        print("❌ npm not found. Please install npm")
        return False
    
    return True

def setup_backend():
    """Setup the backend environment"""
    print("\n🏗️ Setting up backend...")
    
    backend_dir = Path("backend")
    
    # Create virtual environment
    print("📦 Creating virtual environment...")
    if not (backend_dir / "venv").exists():
        success, stdout, stderr = run_command("python -m venv venv", cwd=backend_dir)
        if not success:
            print(f"❌ Failed to create virtual environment: {stderr}")
            return False
    else:
        print("✅ Virtual environment already exists")
    
    # Set up paths
    if platform.system() == "Windows":
        venv_pip = str(backend_dir / "venv" / "Scripts" / "pip.exe")
    else:
        venv_pip = str(backend_dir / "venv" / "bin" / "pip")
    
    # Install requirements
    print("📚 Installing Python dependencies...")
    requirements_path = str(backend_dir / "requirements.txt")
    pip_command = f'"{venv_pip}" install -r "{requirements_path}"'
    success, stdout, stderr = run_command(pip_command, shell=True)
    if not success:
        print(f"❌ Failed to install requirements: {stderr}")
        return False
    
    # Create .env file if it doesn't exist
    env_file = backend_dir / ".env"
    env_example = backend_dir / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file...")
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("⚠️  Please edit backend/.env and add your Google Gemini API key!")
    
    print("✅ Backend setup complete!")
    return True

def setup_frontend():
    """Setup the frontend environment"""
    print("\n🎨 Setting up frontend...")
    
    frontend_dir = Path("frontend")
    
    # Install npm dependencies
    print("📦 Installing Node.js dependencies...")
    success, stdout, stderr = run_command("npm install", cwd=frontend_dir)
    if not success:
        print(f"❌ Failed to install npm dependencies: {stderr}")
        return False
    
    print("✅ Frontend setup complete!")
    return True

def create_sample_data():
    """Create sample data directory and files"""
    print("\n📄 Setting up sample data...")
    
    data_dir = Path("data")
    if not data_dir.exists():
        data_dir.mkdir()
        print("✅ Created data directory")
    
    # The sample CSV is already created by the file creation above
    print("✅ Sample data ready!")
    return True

def print_next_steps():
    """Print instructions for next steps"""
    print("\n🎉 Setup Complete!")
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    
    print("\n1. 🔑 Get your Google Gemini API Key:")
    print("   - Visit: https://makersuite.google.com/app/apikey")
    print("   - Create a new API key")
    print("   - Add it to backend/.env file")
    
    print("\n2. 🚀 Run the application:")
    print("   Terminal 1 (Backend):")
    if platform.system() == "Windows":
        print("   cd backend")
        print("   venv\\Scripts\\activate")
        print("   python main.py")
    else:
        print("   cd backend")
        print("   source venv/bin/activate")
        print("   python main.py")
    
    print("\n   Terminal 2 (Frontend):")
    print("   cd frontend")
    print("   npm start")
    
    print("\n3. 🌐 Open your browser:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    
    print("\n4. 📊 Try uploading the sample data:")
    print("   - Use the file: data/hero_vida_sales_data.csv")
    print("   - Ask questions about Hero Vida strategy!")
    
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("🏗️  Hero Vida RAG Application Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Setup failed! Please install the required software first.")
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed!")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed!")
        sys.exit(1)
    
    # Create sample data
    create_sample_data()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
