# IronClaw Platform: Token Economics, Model Margins & Financial Architecture

## 1. Token Cost Modeling by Model Tier

IronClaw leverages an intelligent multi-model routing strategy to maximize output quality while minimizing inference expenditure.

```
                               ┌────────────────────────────────┐
                               │   USER QUERY / AGENT TASK      │
                               └───────────────┬────────────────┘
                                               │
                                               ▼
                              ┌──────────────────────────────────┐
                              │     INTELLIGENT MODEL ROUTER     │
                              │  • Intent analysis & difficulty  │
                              │  • Context & token estimation    │
                              └───────┬──────────────┬───────────┘
                                      │              │
                   ┌──────────────────┘              └──────────────────┐
                   ▼                                                    ▼
    ┌─────────────────────────────┐                      ┌─────────────────────────────┐
    │     TIER 1: FAST ENGINE     │                      │   TIER 2: REASONING & CODE  │
    │  (google/gemini-2.0-flash)  │                      │ (claude-3.5-sonnet / ds-r1) │
    │  • Tool routing & web search│                      │ • Complex code execution    │
    │  • Email parsing & summaries│                      │ • Multi-step architecture   │
    │  • $0.10 / $0.40 per 1M tok │                      │ • $3.00 / $15.00 per 1M tok │
    │  • Cost: $0.00031 / turn    │                      │ • Cost: $0.0092 / turn      │
    └─────────────────────────────┘                      └─────────────────────────────┘
```

---

## 2. Unit Economics per Subscription Tier

| Tier | Price | Max Daily Quota | Est. Average Usage | Monthly COGS (Blended) | Net Margin | Gross Profit |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Starter** | **$9.99 / mo** | 300 turns / day | 2,500 turns / mo | **$2.45** | **75.5%** | **+$7.54 / user** |
| **Pro** | **$29.99 / mo** | 1,500 turns / day | 8,000 turns / mo | **$7.80** | **74.0%** | **+$22.19 / user** |
| **Enterprise** | **$99.99 / mo** | 10,000 turns / day | 30,000 turns / mo | **$26.10** | **73.9%** | **+$73.89 / user** |

---

## 3. Financial Projections (SaaS Growth Model)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          12-MONTH REVENUE & MARGIN SCALING                      │
├─────────────────┬──────────────┬──────────────┬────────────────┬────────────────┤
│ Metric          │ Month 1      │ Month 3      │ Month 6        │ Month 12       │
├─────────────────┼──────────────┼──────────────┼────────────────┼────────────────┤
│ Active Users    │ 50           │ 250          │ 1,000          │ 5,000          │
│ Paying Subs     │ 15           │ 85           │ 380            │ 2,100          │
│ Monthly MRR     │ $420.00      │ $2,450.00    │ $11,200.00     │ $62,500.00     │
│ Blended COGS    │ $105.00      │ $615.00      │ $2,800.00      │ $15,600.00     │
│ Server & Infra  │ $20.00       │ $45.00       │ $120.00        │ $450.00        │
│ Net Profit (Mo) │ **+$295.00** │ **+$1,790.00**│ **+$8,280.00** │ **+$46,450.00**│
│ Gross Margin %  │ **75.0%**    │ **74.9%**    │ **75.0%**      │ **74.5%**      │
└─────────────────┴──────────────┴──────────────┴────────────────┴────────────────┘
```

---

## 4. Quota Enforcement & Cost Protection Rules

1. **Daily Reset**: Quotas reset at `00:00 UTC` daily.
2. **Hard Token Cap**: Agent executions automatically truncate past 8,000 output tokens to prevent runaway loops.
3. **SSRF & Network Shield**: External tool calls timeout after 15s; memory searches use indexed PostgreSQL full-text scanning to prevent unbounded DB latency.
