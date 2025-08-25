# 🚀 Deployment Guide - Hero Vida RAG Application

## 🎯 Deployment Strategy

We'll use **free cloud services** for a production-ready deployment:
- **Backend**: Railway (FastAPI + ChromaDB + Gemini)
- **Frontend**: Vercel (React app)

## 📋 Prerequisites

1. ✅ Working local application
2. ✅ Google Gemini API key
3. ✅ GitHub account (for deployment)
4. ✅ Railway account (free tier)
5. ✅ Vercel account (free tier)

## 🏗️ Step-by-Step Deployment

### Step 1: Create GitHub Repository

1. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Name: `hero-vida-rag-app`
   - Set to Public (required for free deployments)
   - Don't initialize with README

2. **Push your code to GitHub:**
   ```cmd
   # Initialize git in project directory
   git init
   git add .
   git commit -m "Initial commit: Hero Vida RAG Application"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/hero-vida-rag-app.git
   git push -u origin main
   ```

### Step 2: Deploy Backend to Railway

1. **Go to Railway:**
   - Visit: https://railway.app
   - Sign up/Login with GitHub

2. **Create New Project:**
   - Click "New Project"
   - Choose "Deploy from GitHub repo"
   - Select your `hero-vida-rag-app` repository
   - Choose "Deploy"

3. **Configure Environment Variables:**
   - Go to your deployed service
   - Click "Variables" tab
   - Add these variables:
     ```
     GOOGLE_API_KEY=your_actual_gemini_api_key
     FRONTEND_URL=https://your-app-name.vercel.app
     CHROMA_DB_PATH=/app/chroma_db
     MAX_FILE_SIZE=31457280
     CHUNK_SIZE=1000
     CHUNK_OVERLAP=200
     ```

4. **Set Root Directory:**
   - In Railway settings, set "Root Directory" to `backend`

5. **Get Your Backend URL:**
   - Copy the Railway deployment URL (e.g., `https://your-service.railway.app`)

### Step 3: Deploy Frontend to Vercel

1. **Go to Vercel:**
   - Visit: https://vercel.com
   - Sign up/Login with GitHub

2. **Import Project:**
   - Click "New Project"
   - Import your GitHub repository
   - Set "Root Directory" to `frontend`
   - Click "Deploy"

3. **Configure Environment Variables:**
   - In Vercel dashboard, go to Settings > Environment Variables
   - Add:
     ```
     REACT_APP_API_URL=https://your-railway-backend-url.railway.app
     SKIP_PREFLIGHT_CHECK=true
     GENERATE_SOURCEMAP=false
     ```

4. **Redeploy:**
   - Go to Deployments tab
   - Click "Redeploy" to apply environment variables

### Step 4: Update CORS Configuration

1. **Update Backend CORS:**
   - In Railway, update the `FRONTEND_URL` variable to your Vercel URL
   - Example: `FRONTEND_URL=https://hero-vida-rag-app.vercel.app`

2. **Redeploy Backend:**
   - Railway will auto-redeploy when you update environment variables

## 🔧 Deployment Files Created

### Backend Deployment Files:
- ✅ `backend/Dockerfile` - Container configuration
- ✅ `backend/railway.toml` - Railway deployment config
- ✅ `backend/requirements-prod.txt` - Production dependencies

### Frontend Deployment Files:
- ✅ `frontend/vercel.json` - Vercel deployment config
- ✅ `frontend/.env` - Development environment variables

## 🌐 Expected URLs

After deployment, you'll get:
- **Backend API**: `https://your-service-name.railway.app`
- **Frontend App**: `https://your-app-name.vercel.app`
- **API Docs**: `https://your-service-name.railway.app/docs`

## ✅ Verification Steps

### Test Backend Deployment:
1. Visit: `https://your-backend-url.railway.app/health`
2. Should return: `{"status": "healthy", "service": "Hero Vida RAG API"}`
3. Visit: `https://your-backend-url.railway.app/docs` for API documentation

### Test Frontend Deployment:
1. Visit your Vercel URL
2. Upload a test CSV file
3. Try the chat functionality
4. Verify responses work correctly

### Test End-to-End:
1. Upload documents in the deployed app
2. Ask questions and get AI responses
3. Check database statistics
4. Verify source attribution works

## 🎯 What Your Boss Will See

**Direct Link**: Share your Vercel URL (e.g., `https://hero-vida-rag-app.vercel.app`)

**Features Available:**
- ✅ Professional UI with Hero Vida branding
- ✅ Drag & drop file upload (up to 30MB)
- ✅ ChatGPT-like interface for questions
- ✅ Real-time database statistics
- ✅ Source attribution for all responses
- ✅ Mobile-responsive design

## 🔒 Security & Performance

### Production Optimizations:
- ✅ CORS properly configured for cross-domain access
- ✅ Environment variables secured
- ✅ File size limits enforced
- ✅ Error handling for all edge cases
- ✅ Database persistence across deployments

### Security Features:
- ✅ API key secured in environment variables
- ✅ File type validation
- ✅ File size limits
- ✅ CORS protection
- ✅ Error message sanitization

## 💰 Cost Breakdown

### Free Tier Limits:
- **Railway**: 500 execution hours/month (sufficient for demos)
- **Vercel**: Unlimited for personal projects
- **Total Cost**: $0/month for development and demo usage

### If You Need More Resources:
- Railway Pro: $5/month for more execution hours
- Vercel Pro: $20/month for team features

## 🚀 Quick Deploy Commands

If you want to automate deployment, here are the essential commands:

```bash
# 1. Setup git repository
git init
git add .
git commit -m "Deploy Hero Vida RAG App"
git remote add origin https://github.com/USERNAME/hero-vida-rag-app.git
git push -u origin main

# 2. Deploy backend to Railway
# (Done through Railway web interface)

# 3. Deploy frontend to Vercel  
# (Done through Vercel web interface)
```

## 🎉 Success Indicators

### Deployment Successful When:
- ✅ Backend health check returns 200 OK
- ✅ Frontend loads without errors
- ✅ File upload works in production
- ✅ Chat responses generated successfully
- ✅ Database stats update correctly
- ✅ CORS allows cross-domain requests

---

## 🏆 Ready for Your Boss!

Once deployed, you'll have:
1. **Professional shareable link** for immediate access
2. **No local setup required** - works on any device
3. **Persistent data storage** - uploaded files remain available
4. **Production-grade performance** - fast and reliable
5. **Mobile-friendly interface** - works on phones/tablets

**Your boss can start using the application immediately by visiting the Vercel URL!**
