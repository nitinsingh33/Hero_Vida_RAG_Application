#!/usr/bin/env python3
"""
Automated deployment script for Hero Vida RAG Application
This script guides you through deploying to Railway (backend) and Vercel (frontend)
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_git():
    """Check if git is available"""
    success, stdout, stderr = run_command("git --version")
    if success:
        print(f"✅ Git: {stdout.strip()}")
        return True
    else:
        print("❌ Git not found. Please install Git first.")
        return False

def setup_git_repo():
    """Initialize git repository and prepare for deployment"""
    print("\n🔧 Setting up Git repository...")
    
    # Check if already a git repo
    if Path(".git").exists():
        print("✅ Git repository already initialized")
    else:
        success, stdout, stderr = run_command("git init")
        if not success:
            print(f"❌ Failed to initialize git: {stderr}")
            return False
        print("✅ Git repository initialized")
    
    # Add all files
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"❌ Failed to add files: {stderr}")
        return False
    
    # Check if there are changes to commit
    success, stdout, stderr = run_command("git status --porcelain")
    if stdout.strip():
        # Commit changes
        success, stdout, stderr = run_command('git commit -m "Prepare Hero Vida RAG App for deployment"')
        if not success:
            print(f"❌ Failed to commit: {stderr}")
            return False
        print("✅ Changes committed")
    else:
        print("✅ No changes to commit")
    
    return True

def create_github_instructions():
    """Provide instructions for GitHub setup"""
    print("\n📋 GitHub Setup Instructions:")
    print("="*60)
    print("1. Go to: https://github.com/new")
    print("2. Repository name: hero-vida-rag-app")
    print("3. Set to PUBLIC (required for free deployments)")
    print("4. Do NOT initialize with README")
    print("5. Click 'Create repository'")
    print("6. Copy the repository URL (e.g., https://github.com/username/hero-vida-rag-app.git)")
    print("="*60)
    
    repo_url = input("\n📝 Enter your GitHub repository URL: ").strip()
    
    if not repo_url:
        print("❌ Repository URL is required")
        return None
    
    # Add remote and push
    print(f"\n🚀 Pushing to GitHub: {repo_url}")
    
    # Remove existing remote if it exists
    run_command("git remote remove origin")
    
    # Add new remote
    success, stdout, stderr = run_command(f'git remote add origin {repo_url}')
    if not success:
        print(f"❌ Failed to add remote: {stderr}")
        return None
    
    # Push to GitHub
    success, stdout, stderr = run_command("git push -u origin main")
    if not success:
        # Try creating main branch first
        run_command("git branch -M main")
        success, stdout, stderr = run_command("git push -u origin main")
        if not success:
            print(f"❌ Failed to push to GitHub: {stderr}")
            return None
    
    print("✅ Code pushed to GitHub successfully!")
    return repo_url

def deploy_to_railway():
    """Provide Railway deployment instructions"""
    print("\n🚂 Railway Backend Deployment:")
    print("="*60)
    print("1. Go to: https://railway.app")
    print("2. Sign up/Login with GitHub")
    print("3. Click 'New Project' → 'Deploy from GitHub repo'")
    print("4. Select your 'hero-vida-rag-app' repository")
    print("5. Click 'Deploy'")
    print("6. Once deployed, go to your service")
    print("7. Click 'Settings' → Set 'Root Directory' to 'backend'")
    print("8. Click 'Variables' tab and add these environment variables:")
    print("   GOOGLE_API_KEY=your_actual_gemini_api_key")
    print("   CHROMA_DB_PATH=/app/chroma_db")
    print("   MAX_FILE_SIZE=31457280")
    print("   CHUNK_SIZE=1000")
    print("   CHUNK_OVERLAP=200")
    print("9. Copy your Railway URL (e.g., https://xyz.railway.app)")
    print("="*60)
    
    # Open Railway in browser
    webbrowser.open("https://railway.app")
    
    backend_url = input("\n📝 Enter your Railway backend URL (after deployment): ").strip()
    return backend_url

def deploy_to_vercel(backend_url):
    """Provide Vercel deployment instructions"""
    print("\n⚡ Vercel Frontend Deployment:")
    print("="*60)
    print("1. Go to: https://vercel.com")
    print("2. Sign up/Login with GitHub")
    print("3. Click 'New Project'")
    print("4. Import your GitHub repository")
    print("5. Set 'Root Directory' to 'frontend'")
    print("6. Click 'Deploy'")
    print("7. After deployment, go to Settings → Environment Variables")
    print("8. Add these environment variables:")
    print(f"   REACT_APP_API_URL={backend_url}")
    print("   SKIP_PREFLIGHT_CHECK=true")
    print("   GENERATE_SOURCEMAP=false")
    print("9. Go to Deployments → Click 'Redeploy' to apply variables")
    print("10. Copy your Vercel URL (e.g., https://your-app.vercel.app)")
    print("="*60)
    
    # Open Vercel in browser
    webbrowser.open("https://vercel.com")
    
    frontend_url = input("\n📝 Enter your Vercel frontend URL (after deployment): ").strip()
    return frontend_url

def update_cors_config(backend_url, frontend_url):
    """Update CORS configuration with production URLs"""
    print(f"\n🔧 Updating CORS configuration...")
    print("Go back to Railway and update the FRONTEND_URL variable:")
    print(f"FRONTEND_URL={frontend_url}")
    print("This will automatically redeploy your backend with correct CORS settings.")
    
    input("\nPress Enter after updating the FRONTEND_URL in Railway...")
    print("✅ CORS configuration updated!")

def create_deployment_summary(backend_url, frontend_url):
    """Create a summary of deployed application"""
    summary = f"""
# 🎉 Deployment Complete - Hero Vida RAG Application

## 🌐 Live Application URLs

### 🎯 **Main Application (Share this with your boss):**
**{frontend_url}**

### 🔧 **Backend API:**
**{backend_url}**

### 📚 **API Documentation:**
**{backend_url}/docs**

---

## 🚀 **How Your Boss Can Use It:**

1. **Visit the main application:** {frontend_url}
2. **Upload Documents:** 
   - Click "Upload Documents" tab
   - Drag & drop PDF or CSV files (up to 30MB)
   - Wait for processing confirmation
3. **Chat with Data:**
   - Go to "Chat" tab
   - Ask questions about Hero Vida strategy
   - Get AI-powered responses with source attribution
4. **Monitor Database:**
   - Check "Database" tab for statistics
   - View uploaded documents and data chunks

---

## 📊 **Sample Questions for Demo:**
- "What are Hero Vida's revenue projections for 2024?"
- "What are the key strategic priorities?"
- "How did Hero Vida perform across different regions?"
- "What challenges is Hero Vida facing?"
- "What are the main product models and target segments?"

---

## 🔧 **Technical Details:**
- **Frontend:** React app hosted on Vercel
- **Backend:** FastAPI + ChromaDB hosted on Railway  
- **AI Model:** Google Gemini 1.5 Flash
- **Database:** ChromaDB vector database
- **File Support:** PDF, CSV up to 30MB each
- **Mobile:** Responsive design works on all devices

---

## 🎯 **Key Features:**
✅ Professional ChatGPT-like interface
✅ Drag & drop file upload
✅ Real-time document processing  
✅ AI-powered strategy analysis
✅ Source attribution for transparency
✅ Database statistics and management
✅ Mobile-responsive design

**🏆 Your Hero Vida RAG application is now live and ready for professional use!**
"""
    
    with open("DEPLOYMENT_SUMMARY.md", "w") as f:
        f.write(summary)
    
    print(summary)

def main():
    """Main deployment function"""
    print("🚀 Hero Vida RAG Application - Automated Deployment")
    print("="*70)
    
    # Check requirements
    if not check_git():
        print("\n❌ Please install Git first and try again.")
        sys.exit(1)
    
    # Setup git repository
    if not setup_git_repo():
        print("\n❌ Failed to setup Git repository")
        sys.exit(1)
    
    # GitHub setup
    repo_url = create_github_instructions()
    if not repo_url:
        print("\n❌ GitHub setup failed")
        sys.exit(1)
    
    # Backend deployment
    backend_url = deploy_to_railway()
    if not backend_url:
        print("\n❌ Backend deployment cancelled")
        sys.exit(1)
    
    # Frontend deployment
    frontend_url = deploy_to_vercel(backend_url)
    if not frontend_url:
        print("\n❌ Frontend deployment cancelled")
        sys.exit(1)
    
    # Update CORS
    update_cors_config(backend_url, frontend_url)
    
    # Create summary
    create_deployment_summary(backend_url, frontend_url)
    
    print("\n🎉 Deployment completed successfully!")
    print(f"🌐 Share this link with your boss: {frontend_url}")

if __name__ == "__main__":
    main()
