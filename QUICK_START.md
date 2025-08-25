# 🚀 Quick Start - Hero Vida RAG Application

## ⚠️ IMPORTANT: Navigation First!

Before running the batch files, you must navigate to the project directory:

```cmd
cd "C:\Users\NITIN SINGH\hero-vida-rag-app"
```

## 🎯 Step-by-Step Instructions

### 1. Open Two Command Prompt Windows
- Press `Windows + R`, type `cmd`, press Enter (do this twice)

### 2. Navigate to Project Directory (in both windows)
```cmd
cd "C:\Users\NITIN SINGH\hero-vida-rag-app"
```

### 3. Add Your API Key (First Time Only)
- Edit `backend\.env` file
- Replace `your_gemini_api_key_here` with your actual Gemini API key
- Get key from: https://makersuite.google.com/app/apikey

### 4. Start the Backend (Terminal 1)
```cmd
start_backend.bat
```
**Wait for:** "Hero Vida RAG API is running!" message

### 5. Start the Frontend (Terminal 2)
```cmd
start_frontend.bat
```
**Wait for:** Browser to open automatically at http://localhost:3000

## 🌐 Application URLs
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🎬 Demo Steps
1. **Upload Document**: Go to "Upload Documents" tab
2. **Drag & Drop**: Upload `data\hero_vida_sales_data.csv`
3. **Chat**: Switch to "Chat" tab
4. **Ask Questions**: Try "What are Hero Vida's revenue projections for 2024?"

## 🔍 Verify Everything Works
- ✅ Backend shows "Hero Vida RAG API is running!"
- ✅ Frontend loads at localhost:3000
- ✅ File upload works
- ✅ Chat responses include sources

## 🚨 If Something Goes Wrong
1. Check you're in the right directory: `C:\Users\NITIN SINGH\hero-vida-rag-app`
2. Check both batch files exist: `dir *.bat`
3. Verify API key is set in `backend\.env`
4. See `TROUBLESHOOTING.md` for detailed help

---
**🏆 Ready to revolutionize document analysis with AI!**
