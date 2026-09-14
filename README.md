# EnterpriseIQ

AI finance and sales intelligence agent. A FastAPI backend that answers questions
over financial documents and CRM data, forecasts revenue, and triggers follow-up
actions — combining retrieval-augmented generation, an LLM, a small ML model and
MCP-style tool calls.

## What it does

- **Ask** natural-language questions over finance and sales documents, answered
  from retrieved context rather than model memory
- **Analyse** uploaded documents, surface KPIs, and flag anomalies in the numbers
- **Forecast** revenue from historical pipeline data
- **Act** on the result — send a report, schedule a meeting

## Tech stack

| Layer | What it does |
| --- | --- |
| FastAPI + Uvicorn | HTTP API and app lifecycle |
| RAG service | Retrieves relevant document chunks to ground each answer |
| LLM service | Claude API calls for reasoning and generation |
| ML service | scikit-learn model behind the revenue forecast |
| MCP service | Tool-call layer for the action endpoints |
| Railway | Deployment target (`Procfile` + `railway.toml`) |

## Repository layout

```
OneDrive/Desktop/enterpriseiq/
├── backend/
│   ├── main.py              # FastAPI app, CORS, router registration
│   ├── routers/             # chat, analysis, forecast, actions
│   ├── services/            # rag, llm, ml, mcp
│   ├── requirements.txt
│   ├── Procfile             # web: uvicorn main:app
│   └── railway.toml
└── frontend/
    └── index.html           # single-page UI
```

> **Note on that path.** The application currently lives under
> `OneDrive/Desktop/enterpriseiq/` because a local sync folder was committed
> along with the project. Everything works, but `backend/` and `frontend/`
> belong at the repository root. Moving them is a single `git mv` and would let
> CI and deployment configs drop the long prefix.

## Getting started

**Prerequisites:** Python 3.11 and an Anthropic API key.

```bash
cd OneDrive/Desktop/enterpriseiq/backend

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env             # then add your key
```

`.env` needs one value:

```
ANTHROPIC_API_KEY=sk-ant-...
```

Run it:

```bash
uvicorn main:app --reload
```

The API comes up on `http://127.0.0.1:8000`. Interactive docs are at
`http://127.0.0.1:8000/docs`, and `GET /` returns a status payload.

For the UI, open `frontend/index.html` in a browser.

## API

All routes are prefixed with `/api`.

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/chat/ask` | Ask a question; answered from retrieved context |
| `POST` | `/api/analysis/document` | Analyse a supplied document |
| `POST` | `/api/analysis/report` | Generate a written report |
| `GET` | `/api/analysis/kpis` | Current KPI summary |
| `GET` | `/api/analysis/anomalies` | Anomalies detected in the data |
| `POST` | `/api/forecast/revenue` | Produce a revenue forecast |
| `GET` | `/api/forecast/revenue` | Retrieve the last forecast |
| `POST` | `/api/actions/send-report` | Email a report |
| `POST` | `/api/actions/schedule-meeting` | Schedule a follow-up meeting |

## Deployment

Railway, using the committed `Procfile`:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Set `ANTHROPIC_API_KEY` in the Railway environment. `PORT` is injected by the
platform.

## Continuous integration

`.github/workflows/ci.yml` runs on every push and pull request against `main`:
dependency install, flake8 (syntax and undefined-name errors are hard failures,
style issues are reported but non-blocking), and pytest when a `tests/`
directory is present.

## License

MIT
