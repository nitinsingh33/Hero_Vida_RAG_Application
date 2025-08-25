# 🚀 Deploy Your Hero Vida RAG App - Step by Step

**Total Time: ~15 minutes | Cost: FREE**

## 🎯 What You'll Get
- **Live URL** to share with your boss
- **Professional interface** accessible from anywhere
- **No setup required** for users

---

## 📋 **Step 1: Create GitHub Account & Repository (5 min)**

### 1.1 Create GitHub Account (if needed)
- Go to: https://github.com
- Sign up with your email

### 1.2 Create New Repository
1. Click the **"+"** icon → **"New repository"**
2. **Repository name:** `hero-vida-rag-app`
3. **Visibility:** Set to **PUBLIC** (required for free deployment)
4. **DO NOT** check "Add a README file"
5. Click **"Create repository"**
6. **Copy the repository URL** (looks like: `https://github.com/yourusername/hero-vida-rag-app.git`)

---

## 📤 **Step 2: Push Code to GitHub (2 min)**

Run these commands in your project directory:

```cmd
# Navigate to your project (if not already there)
cd "C:\Users\NITIN SINGH\hero-vida-rag-app"

# Initialize git and push
git add .
git commit -m "Deploy Hero Vida RAG Application"
git branch -M main
git remote add origin https://github.com/YOURUSERNAME/hero-vida-rag-app.git
git push -u origin main
```

**Replace `YOURUSERNAME` with your actual GitHub username!**

---

## 🚂 **Step 3: Deploy Backend to Railway (5 min)**

### 3.1 Create Railway Account
1. Go to: https://railway.app
2. Click **"Login"** → **"Login with GitHub"**
3. Authorize Railway to access your GitHub

### 3.2 Deploy Backend
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your **`hero-vida-rag-app`** repository
4. Click **"Deploy"**
5. Wait for initial deployment to complete

### 3.3 Configure Backend
1. Click on your deployed service
2. Go to **"Settings"** tab
3. Set **"Root Directory"** to `backend`
4. Go to **"Variables"** tab
5. Add these environment variables:
   ```
   GOOGLE_API_KEY=your_actual_gemini_api_key_here
   CHROMA_DB_PATH=/app/chroma_db
   MAX_FILE_SIZE=31457280
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   ```
6. **Copy your Railway URL** (e.g., `https://web-production-abc123.up.railway.app`)

---

## ⚡ **Step 4: Deploy Frontend to Vercel (3 min)**

### 4.1 Create Vercel Account
1. Go to: https://vercel.com
2. Click **"Sign Up"** → **"Continue with GitHub"**
3. Authorize Vercel

### 4.2 Deploy Frontend
1. Click **"New Project"**
2. **Import** your GitHub repository
3. **Root Directory:** Set to `frontend`
4. Click **"Deploy"**
5. Wait for deployment to complete

### 4.3 Configure Frontend
1. Go to **"Settings"** → **"Environment Variables"**
2. Add these variables:
   ```
   REACT_APP_API_URL=your_railway_backend_url_here
   SKIP_PREFLIGHT_CHECK=true
   GENERATE_SOURCEMAP=false
   ```
3. Go to **"Deployments"** → Click **"Redeploy"** button
4. **Copy your Vercel URL** (e.g., `https://hero-vida-rag-app.vercel.app`)

---

## 🔧 **Step 5: Final Configuration (1 min)**

### 5.1 Update Backend CORS
1. Go back to **Railway**
2. In **"Variables"** tab, add:
   ```
   FRONTEND_URL=your_vercel_frontend_url_here
   ```
3. This will automatically redeploy your backend

---

## ✅ **Step 6: Test Your Deployment**

### 6.1 Test Backend
- Visit: `your-railway-url/health`
- Should show: `{"status": "healthy", "service": "Hero Vida RAG API"}`

### 6.2 Test Frontend
- Visit your Vercel URL
- Should load the Hero Vida RAG interface

### 6.3 Test End-to-End
1. Upload a test CSV file
2. Ask a question in chat
3. Verify you get AI responses with sources

---

## 🎉 **SUCCESS! Your App is Live**

### 🌐 **Share These URLs:**
- **Main App:** `https://your-app.vercel.app` ← **Share this with your boss**
- **API Docs:** `https://your-backend.railway.app/docs`

### 🎯 **What Your Boss Can Do:**
✅ Upload Hero Vida strategy documents (PDF/CSV)  
✅ Ask strategic questions via ChatGPT-like interface  
✅ Get AI-powered insights with source attribution  
✅ Monitor database and document statistics  
✅ Access from any device (mobile-friendly)  

---

## 🚨 **If Something Goes Wrong:**

### Common Issues:
1. **"Repository not found"** → Check GitHub URL is correct
2. **"Build failed"** → Check all files are pushed to GitHub
3. **"API not responding"** → Verify environment variables in Railway
4. **"CORS error"** → Update FRONTEND_URL in Railway variables

### Quick Fixes:
- **Redeploy backend:** Railway → Deployments → Redeploy
- **Redeploy frontend:** Vercel → Deployments → Redeploy
- **Check logs:** Look at deployment logs in Railway/Vercel dashboards

---

## 💰 **Cost: $0/month**
- Railway: 500 execution hours/month (FREE)
- Vercel: Unlimited static hosting (FREE)
- Perfect for demos and professional presentations!

---

**🏆 Your Hero Vida RAG application is now live and ready to impress your boss!**
