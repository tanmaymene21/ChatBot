# 🤖 Product & Supplier Chatbot

> *Your inventory at your fingertips, just a conversation away!*

An intelligent conversational assistant that transforms how you interact with your product catalog and supplier network. Powered by natural language processing and built with technologies like FastAPI, React, and LangGraph, this system breaks down the barriers between you and your data.

## ✨ Features

### 🧠 Core Intelligence
- **Natural Language Understanding**: Chat with your data as naturally as texting a colleague
- **Real-Time Interaction**: Instant responses with smooth, chat-like experience
- **Secure Access**: JWT authentication keeps your data safe
- **Memory That Persists**: Never lose valuable conversations with persistent history
- **Smart Data Retrieval**: Efficiently pulls structured information from PostgreSQL

### 🔍 Query Superpowers
- **Smart Product Search**: Find exactly what you need by brand, category, or price
- **Supplier Discovery**: Instantly match suppliers with product categories
- **Deep Product Insights**: Get comprehensive product details in seconds
- **Supplier Network**: Explore your supplier ecosystem and their offerings

## 🛠️ Technology Stack

### 🔧 Backend 
- **Framework**: FastAPI - lightning-fast API development
- **Database**: PostgreSQL - rock-solid data storage
- **ORM**: SQLAlchemy - elegant database interactions
- **Authentication**: JWT - industry-standard security
- **AI/ML**: 
  - LangGraph for sophisticated conversation flows
  - Open-source LLM integration via Groq for natural language understanding

### 🎨 Frontend 
- **Framework**: React
- **Styling**: Tailwind CSS 
- **State Management**: Context API 
- **HTTP Client**: Axios 
- **UI Components**: Custom-built for perfect user experience

### 📊 Data Architecture
- **Products**: Comprehensive product information including ID, name, brand, price, category, description, and supplier relationships
- **Suppliers**: Complete supplier profiles with contact details and specialty categories
- **Conversation History**: Intelligent storage of user interactions for context preservation

## 🚀 Getting Started

### 📥 Installation

1. **Clone your way to innovation**
```bash
git clone https://github.com/tanmaymene21/ChatBot.git
```

2. **Prepare your backend command center**
```bash
cd backend
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```

3. **Set up your frontend experience**
```bash
cd frontend
npm install
```

4. **Configure your environment**
Create `.env` file in backend directory with your digital keys:
```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. **Launch your services**

**Backend:**
```bash
cd backend
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

## 💬 Conversation Examples

Your new digital assistant understands queries like these and much more:

### 📦 Product Explorations
- "Show me all products"
- "Show me all Electronics products"
- "What gaming products do you have?"
- "List all accessories"
- "Can I get a list of all furniture items?"
- "Show me all products under brand TechMaster"

### 🏭 Supplier Intelligence
- "Show me all suppliers"
- "Which suppliers provide electronics?"
- "Tell me about supplier XYZ"
- "What products does supplier ABC offer?"

---

*Transform your inventory management with the power of conversation - where data meets dialogue!*