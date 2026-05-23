"""
RAG Service — Finance & Sales Knowledge Base
Retrieves relevant business context for any query
"""

from typing import List, Dict, Any

BUSINESS_KNOWLEDGE = [
    {
        "id": "sales_001",
        "source": "Sales Performance Framework",
        "category": "sales",
        "content": "Q3 2024 Regional Performance: North America $4.2M (↑12% YoY), EMEA $2.8M (↓3% YoY), APAC $1.9M (↑28% YoY). Top performing product: Enterprise Suite at $3.1M. Underperforming: Legacy Basic tier at $0.4M (↓22%). Overall Q3 revenue: $8.9M vs $8.2M target — 108% attainment."
    },
    {
        "id": "sales_002",
        "source": "Sales Pipeline Report",
        "category": "sales",
        "content": "Current pipeline: $24.3M total. Stage breakdown: Prospecting $8.1M (33%), Qualification $5.2M (21%), Proposal $4.8M (20%), Negotiation $3.9M (16%), Closing $2.3M (9%). Win rate: 23% overall, 41% from Negotiation stage. Average deal size: $47K. Average sales cycle: 67 days."
    },
    {
        "id": "sales_003",
        "source": "Customer Analytics Report",
        "category": "customers",
        "content": "Customer base: 312 active accounts. Top 10 customers = 38% of revenue. Churn rate: 4.2% quarterly (industry avg: 5.1%). Net Revenue Retention: 118%. Average contract value: $28.4K/year. Customer acquisition cost: $12.3K. LTV:CAC ratio: 4.6x. New logos Q3: 23."
    },
    {
        "id": "finance_001",
        "source": "P&L Summary Q3 2024",
        "category": "finance",
        "content": "Q3 2024 Financials: Revenue $8.9M, COGS $2.7M, Gross Profit $6.2M (70% margin). Operating expenses: Sales & Marketing $2.1M, R&D $1.8M, G&A $0.9M. EBITDA $1.4M (16% margin). Net Income $1.1M. Cash position: $12.4M. Burn rate: $0.8M/month (if needed)."
    },
    {
        "id": "finance_002",
        "source": "Budget vs Actual Report",
        "category": "finance",
        "content": "YTD Budget vs Actual: Revenue $24.1M actual vs $22.8M budget (+5.7%). Sales costs $5.9M vs $5.4M budget (+9.3% over). R&D $5.2M vs $5.5M budget (-5.5% under). G&A $2.6M vs $2.8M budget (-7.1% under). Net: $0.8M ahead of profit plan. Q4 revised forecast: $9.6M revenue."
    },
    {
        "id": "finance_003",
        "source": "Cash Flow Statement",
        "category": "finance",
        "content": "Operating cash flow Q3: $1.8M positive. Key items: Collections improved — DSO down from 52 to 44 days. Deferred revenue increased $0.4M (strong prepayments). CapEx: $0.2M (infrastructure). Free cash flow: $1.6M. 12-month runway: 15+ months at current burn. No debt outstanding."
    },
    {
        "id": "product_001",
        "source": "Product Revenue Breakdown",
        "category": "products",
        "content": "Product mix Q3: Enterprise Suite $3.1M (35%), Professional $2.4M (27%), Growth $1.8M (20%), Starter $1.2M (13%), Legacy Basic $0.4M (5%). Enterprise Suite growing fastest at +34% YoY. Legacy Basic declining -22% — customers migrating up. Professional tier showing 18% expansion revenue from upsells."
    },
    {
        "id": "product_002",
        "source": "Product Usage & Health Metrics",
        "category": "products",
        "content": "Product engagement: DAU/MAU ratio 0.68 (healthy). Feature adoption: Core features 94%, Advanced analytics 61%, API integrations 43%, Mobile app 38%. NPS score: 52 (up from 44 last quarter). Support tickets: 1,240 Q3 (-8% QoQ). CSAT: 4.3/5. Avg onboarding time: 8 days (down from 14)."
    },
    {
        "id": "team_001",
        "source": "Sales Team Performance",
        "category": "team",
        "content": "Sales team: 18 AEs total. Top quartile (5 reps): avg $620K/quarter. Mid performers (9 reps): avg $290K/quarter. Under performers (4 reps): avg $95K/quarter. Quota attainment: 67% of team above quota. New hire ramp: 5 months avg to full productivity. Voluntary attrition: 2 AEs departed Q3."
    },
    {
        "id": "market_001",
        "source": "Competitive Intelligence Report",
        "category": "market",
        "content": "Market position: #3 in mid-market segment (11% share). Main competitors: CompetitorA (23% share, enterprise focus), CompetitorB (18% share, SMB focus). Win/loss vs CompetitorA: 34% win rate. Win/loss vs CompetitorB: 61% win rate. Key differentiators: Ease of use, customer support, API flexibility. Lost deals: 38% on price, 29% on features, 33% chose status quo."
    },
    {
        "id": "forecast_001",
        "source": "Q4 2024 Forecast",
        "category": "forecast",
        "content": "Q4 forecast: Base case $9.6M (↑8% QoQ), Upside $10.8M, Downside $8.4M. Key assumptions: 3 enterprise deals ($1.2M combined) expected to close. APAC expansion adding $0.3M incremental. Risk: 2 large renewals ($0.8M) at risk — competitive situation. Pipeline coverage: 3.2x (healthy). Confidence: 74%."
    },
    {
        "id": "risk_001",
        "source": "Risk Register",
        "category": "risks",
        "content": "Key business risks: (1) Customer concentration — top 3 customers = 18% revenue, renewal Q1. (2) Competitive displacement in EMEA — CompetitorA aggressive pricing. (3) Sales capacity — 2 open AE headcount, Q4 targets at risk. (4) Product gap — enterprise SSO feature requested by 12 accounts worth $2.1M. (5) Macro risk — 3 prospects citing budget freezes."
    },
]


class RAGService:
    def __init__(self):
        self._index: list = []

    async def initialize(self):
        self._index = BUSINESS_KNOWLEDGE
        print(f"📚 RAG service ready — {len(BUSINESS_KNOWLEDGE)} business knowledge chunks loaded")

    def retrieve(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        query_words = set(query.lower().split())
        scored = []
        for doc in self._index:
            doc_words = set(doc["content"].lower().split())
            overlap = len(query_words & doc_words)
            if overlap > 0:
                scored.append({
                    "content": doc["content"],
                    "source": doc["source"],
                    "category": doc["category"],
                    "score": round(overlap / max(len(query_words), 1), 3),
                })
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k] if scored else [
            {"content": self._index[0]["content"], "source": self._index[0]["source"],
             "category": self._index[0]["category"], "score": 0.1}
        ]
