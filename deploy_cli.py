#!/usr/bin/env python3
"""
CLI-based deployment for Hero Vida RAG Application
This script uses Railway CLI and Vercel CLI for automated deployment
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_cli_tools():
    """Check if required CLI tools are installed"""
    print("🔍 Checking CLI tools...")
    
    tools = {
        "git": "git --version",
        "railway": "railway version", 
        "vercel": "vercel --version"
    }
    
    missing_tools = []
    
    for tool, command in tools.items():
        success, stdout, stderr = run_command(command)
        if success:
            print(f"✅ {tool}: {stdout.strip()}")
        else:
            print(f"❌ {tool}: Not installed")
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"\n📦 Install missing tools:")
        if "railway" in missing_tools:
            print("   Railway CLI: npm install -g @railway/cli")
        if "vercel" in missing_tools:
            print("   Vercel CLI: npm install -g vercel")
        return False
    
    return True

def deploy_backend_cli():
    """Deploy backend using Railway CLI"""
    print("\n🚂 Deploying Backend to Railway...")
    
    # Login to Railway
    print("🔑 Logging into Railway...")
    success, stdout, stderr = run_command("railway login")
    if not success:
        print(f"❌ Railway login failed: {stderr}")
        return False
    
    # Create new project
    print("📦 Creating Railway project...")
    success, stdout, stderr = run_command("railway new", cwd="backend")
    if not success:
        print(f"❌ Failed to create Railway project: {stderr}")
        return False
    
    # Deploy
    print("🚀 Deploying to Railway...")
    success, stdout, stderr = run_command("railway up", cwd="backend")
    if not success:
        print(f"❌ Deployment failed: {stderr}")
        return False
    
    # Get deployment URL
    success, stdout, stderr = run_command("railway status", cwd="backend")
    if success:
        print("✅ Backend deployed successfully!")
        # Extract URL from output (Railway CLI returns the URL)
        lines = stdout.split('\n')
        url = None
        for line in lines:
            if 'https://' in line and 'railway.app' in line:
                url = line.strip()
                break
        if url:
            print(f"🌐 Backend URL: {url}")
            return url
    
    return None

def deploy_frontend_cli(backend_url):
    """Deploy frontend using Vercel CLI"""
    print("\n⚡ Deploying Frontend to Vercel...")
    
    # Create vercel.json with backend URL
    vercel_config = {
        "env": {
            "REACT_APP_API_URL": backend_url,
            "SKIP_PREFLIGHT_CHECK": "true",
            "GENERATE_SOURCEMAP": "false"
        }
    }
    
    with open("frontend/vercel.json", "w") as f:
        json.dump(vercel_config, f, indent=2)
    
    # Login to Vercel
    print("🔑 Logging into Vercel...")
    success, stdout, stderr = run_command("vercel login")
    if not success:
        print(f"❌ Vercel login failed: {stderr}")
        return False
    
    # Deploy
    print("🚀 Deploying to Vercel...")
    success, stdout, stderr = run_command("vercel --prod", cwd="frontend")
    if not success:
        print(f"❌ Deployment failed: {stderr}")
        return False
    
    # Extract URL from output
    lines = stdout.split('\n')
    url = None
    for line in lines:
        if 'https://' in line and 'vercel.app' in line:
            url = line.strip()
            break
    
    if url:
        print(f"✅ Frontend deployed successfully!")
        print(f"🌐 Frontend URL: {url}")
        return url
    
    return None

def main():
    """Main CLI deployment function"""
    print("🚀 Hero Vida RAG Application - CLI Deployment")
    print("="*60)
    
    # Check CLI tools
    if not check_cli_tools():
        print("\n❌ Please install missing CLI tools first.")
        sys.exit(1)
    
    # Setup git
    if not Path(".git").exists():
        run_command("git init")
        run_command("git add .")
        run_command('git commit -m "Initial commit for deployment"')
    
    # Deploy backend
    backend_url = deploy_backend_cli()
    if not backend_url:
        print("\n❌ Backend deployment failed")
        sys.exit(1)
    
    # Deploy frontend
    frontend_url = deploy_frontend_cli(backend_url)
    if not frontend_url:
        print("\n❌ Frontend deployment failed")
        sys.exit(1)
    
    # Success summary
    print("\n🎉 Deployment Complete!")
    print("="*60)
    print(f"🌐 Frontend: {frontend_url}")
    print(f"🔧 Backend: {backend_url}")
    print(f"📚 API Docs: {backend_url}/docs")
    print("="*60)
    print(f"\n🏆 Share this link with your boss: {frontend_url}")

if __name__ == "__main__":
    main()
