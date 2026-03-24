# enterpriseiq
AI Finance &amp; Sales Intelligence Agent — RAG + LLM + ML + MCP
# EnterpriseIQ — AI Finance & Sales Intelligence Agent

> **Production-grade AI system** that connects to business data, analyzes performance, forecasts revenue, and takes autonomous actions — built with RAG + LLM + ML + MCP.

![Claude](https://img.shields.io/badge/Claude%20Sonnet-LLM-blue?style=flat-square)
![RAG](https://img.shields.io/badge/RAG-Retrieval-green?style=flat-square)
![ML](https://img.shields.io/badge/ML-scikit--learn-orange?style=flat-square)
![MCP](https://img.shields.io/badge/MCP-Gmail%20%2B%20Calendar-purple?style=flat-square)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-teal?style=flat-square)

---

## What Problem Does This Solve?

Business leaders waste hours every week on:
- Manually digging through spreadsheets to answer *"Which region underperformed Q3?"*
- Writing executive reports from scratch every month
- Forecasting revenue with basic Excel trendlines
- Scheduling review meetings and emailing reports manually

**EnterpriseIQ solves all of this with AI.**

---

## Architecture

```
enterpriseiq/
├── backend/
│   ├── main.py                      # FastAPI app + lifespan
│   ├── routers/
│   │   ├── chat.py                  # POST /api/chat/ask (RAG + LLM)
│   │   ├── analysis.py              # POST /api/analysis/document|report
│   │   ├── forecast.py              # POST /api/forecast/revenue (ML)
│   │   └── actions.py               # POST /api/actions/send-report|schedule (MCP)
│   └── services/
│       ├── llm_service.py           # Claude Sonnet API wrapper
│       ├── rag_service.py           # Business knowledge base + retrieval
│       ├── ml_service.py            # Revenue forecasting + anomaly detection
│       └── mcp_service.py           # Gmail + Google Calendar via MCP
└── frontend/
    └── index.html                   # Complete dashboard (vanilla JS + Chart.js)
```

---

## AI Stack

| Module | Technology | What It Does |
|--------|-----------|--------------|
| **RAG** | Keyword retrieval | Retrieves relevant business data for any query with cited sources |
| **LLM** | Claude Sonnet | Reasons over context, generates insights and executive reports |
| **ML** | scikit-learn + NumPy | Revenue forecasting + anomaly detection via Z-score analysis |
| **MCP** | Gmail + Google Calendar | Sends reports and creates calendar events autonomously |
| **API** | FastAPI + Python | Production REST API with async endpoints |
| **Frontend** | Vanilla JS + Chart.js | Real-time KPI dashboard and revenue charts |

---

## Features

### 📊 Finance Dashboard
- Real-time KPI cards: YTD revenue, monthly average, QoQ growth
- Revenue trend chart (18 months historical data)
- Product mix breakdown chart
- Risk register with priority flags

### 💬 AI Analyst (RAG + LLM)
- Ask any business question in plain English
- AI retrieves relevant data from 12 business knowledge chunks
- Answers include cited sources
- Quick queries: Region performance, Pipeline status, Q4 risks, Customer health

### 📈 Revenue Forecasting (ML)
- 6-month forward forecast with confidence intervals
- Anomaly detection — flags unusual revenue months
- AI explanation of forecast drivers

### 🔍 Document Intelligence
- Paste any business document — report, email, contract, meeting notes
- Three modes: **Summary**, **Extract KPIs**, **Find Anomalies**

### ⚡ Automated Actions (MCP)
- Send executive reports via Gmail in one click
- Schedule business reviews in Google Calendar
- Generate + email full reports in one workflow

---

## Setup

### 1. Clone and configure
```bash
git clone https://github.com/Manugupranay/enterpriseiq.git
cd enterpriseiq/backend
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

### 2. Install and run backend
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3. Run frontend
```bash
cd ../frontend
python -m http.server 3000 --bind 127.0.0.1
```

### 4. Open browser
```
http://127.0.0.1:3000
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat/ask` | Ask business questions (RAG + LLM) |
| POST | `/api/analysis/document` | Analyze any document |
| GET | `/api/analysis/kpis` | Get current KPIs |
| GET | `/api/analysis/anomalies` | Detect revenue anomalies |
| POST | `/api/forecast/revenue` | ML revenue forecast |
| POST | `/api/actions/send-report` | Send report via Gmail (MCP) |
| POST | `/api/actions/schedule-meeting` | Schedule via Calendar (MCP) |

---

## Production Roadmap

- [ ] Vector DB — ChromaDB or Pinecone for semantic search
- [ ] Real data — Salesforce / HubSpot / SQL connectors
- [ ] Authentication — JWT with role-based access
- [ ] Streaming — SSE for real-time LLM responses
- [ ] Deploy — Docker → Railway / AWS ECS
- [ ] LangGraph — Multi-step agentic reasoning

---

## Author

**Pranay Bhaskar Manugu** — Senior AI/ML Engineer
[LinkedIn](https://linkedin.com/in/pranaybhaskar4870) · [GitHub](https://github.com/Manugupranay)

---

*Built to demonstrate production-grade AI engineering: RAG pipelines, LLM integration, ML forecasting, and MCP agents — all in one system.*
