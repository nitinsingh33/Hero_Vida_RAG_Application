# 🎬 Hero Vida RAG Application Demo

This document provides a step-by-step walkthrough of the Hero Vida RAG application, showing how to upload documents and interact with the AI-powered chat interface.

## 🚀 Quick Demo Setup

### Prerequisites
1. Follow the setup instructions in README.md
2. Get a Google Gemini API key and add it to `backend/.env`
3. Both backend and frontend servers should be running

### Starting the Application

**Terminal 1 - Backend:**
```bash
cd backend
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## 📊 Demo Walkthrough

### Step 1: Access the Application
1. Open your browser and go to `http://localhost:3000`
2. You'll see the Hero Vida RAG Application homepage with a beautiful interface

### Step 2: Upload Sample Data
1. Click on the **"Upload Documents"** tab
2. You'll see a drag-and-drop interface
3. Upload the sample CSV file: `data/hero_vida_sales_data.csv`
4. Watch as the file is processed and chunked for vector storage
5. You should see a success message with processing details

### Step 3: Explore the Database
1. Click on the **"Database"** tab  
2. View statistics showing:
   - Number of documents uploaded
   - Total text chunks created
   - Vector collections
   - List of uploaded files

### Step 4: Chat with Your Data
1. Go to the **"Chat"** tab
2. You'll see a ChatGPT-like interface with suggested questions
3. Try asking these sample questions:

#### Sample Questions to Try:

**Financial Performance:**
```
What were Hero Vida's revenue trends in 2023?
```

**Market Strategy:**
```
What are the key strategic focus areas for Hero Vida?
```

**Growth Projections:**
```
What are the growth targets for 2024?
```

**Challenges:**
```
What are the main challenges Hero Vida is facing?
```

**Regional Performance:**
```
How did Hero Vida perform across different regions?
```

**Product Portfolio:**
```
What product models does Hero Vida offer and their target segments?
```

### Step 5: Observe AI Responses
For each question, notice how the AI:
- Analyzes your uploaded documents
- Provides detailed, contextual answers
- Shows **source attribution** (which documents the answer came from)
- Uses professional business language appropriate for strategy discussions

## 🎯 Expected Demo Outcomes

### Sample Interaction:

**User Question:** "What are Hero Vida's revenue projections for 2024?"

**AI Response:** Based on the uploaded documents, Hero Vida has ambitious revenue projections for 2024:

**Full Year 2024 Financial Projections:**
- **Total Revenue**: ₹706.2 crores (35% growth rate)
- **Quarterly Breakdown**:
  - Q1 2024: ₹125.5 crores
  - Q2 2024: ₹156.2 crores  
  - Q3 2024: ₹189.8 crores
  - Q4 2024: ₹234.7 crores

**Key Growth Drivers:**
- Units sold target: 50,430 units (38% growth)
- Market share target: 25.5% average (8.6 percentage points increase)
- EBITDA margin improvement to 13.0%

The projections show strong growth momentum with revenue growth of 35% and a significant improvement in profitability margins.

**Sources:** hero_vida_sales_data.csv

### Additional Features to Demonstrate:

1. **Multi-turn Conversations**: Ask follow-up questions
2. **Source Attribution**: Show how answers reference specific documents
3. **Markdown Formatting**: Responses include lists, headers, and formatting
4. **Error Handling**: Try asking about topics not in the documents
5. **File Management**: Clear database and re-upload files

## 🔍 Technical Demo Points

### Behind the Scenes:
1. **Document Processing**: PDF/CSV files are parsed and split into chunks
2. **Embedding Generation**: Text chunks are converted to vectors using sentence-transformers
3. **Vector Storage**: ChromaDB stores embeddings for similarity search
4. **RAG Pipeline**: User queries trigger similarity search + Gemini response generation
5. **Real-time UI**: React frontend provides smooth, responsive interface

### Architecture Demonstration:
```
User Query → Vector Search → Retrieve Relevant Chunks → 
Gemini API → Generate Response → Display with Sources
```

## 🎥 Demo Script

### Opening (2 minutes)
"Welcome to the Hero Vida RAG Application demo. This is a cutting-edge Retrieval-Augmented Generation system built specifically for Hero Vida strategy analysis. Let me show you how it works..."

### Upload Demo (3 minutes)  
"First, let's upload some Hero Vida business data. I'll drag this CSV file containing sales data, financial projections, and strategic initiatives..."

### Chat Demo (5 minutes)
"Now comes the exciting part - let's chat with our data. I'll ask about revenue projections... Notice how the AI provides detailed analysis with exact figures and sources..."

### Technical Highlights (2 minutes)
"Behind the scenes, we're using ChromaDB for vector storage, Google Gemini for AI responses, and a modern React interface. The entire pipeline processes documents in real-time..."

### Closing (1 minute)
"This demonstrates how RAG technology can transform business document analysis, making strategic insights instantly accessible through natural language queries."

## 🚨 Demo Troubleshooting

### Common Issues:
1. **No API Key**: Ensure Gemini API key is set in backend/.env
2. **CORS Errors**: Check both servers are running on correct ports
3. **Upload Failures**: Verify file format (PDF/CSV) and size limits
4. **Empty Responses**: Make sure documents were successfully processed

### Pro Tips:
- Upload documents before chatting for best results
- Use specific, strategic questions for better responses  
- Check the Database tab to verify successful uploads
- Try both PDF and CSV files to show versatility

---

**🎉 End of Demo!** 

This RAG application showcases the power of combining modern AI with business document analysis, providing instant access to strategic insights through an intuitive chat interface.
