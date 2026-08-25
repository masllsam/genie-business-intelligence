# IronClaw Platform: Architecture & Infrastructure Specification

## 1. High-Level Architecture Overview

IronClaw is a multi-tenant autonomous AI agent operating system engineered for enterprise and high-frequency autonomous workflows. It provides sandboxed execution environments, persistent conversation workspaces with Thread Context Documents (TCD), structured memories, dynamic tool orchestration, zero-knowledge encrypted artifact generation, and bidirectional email infrastructure.

```
                                    ┌───────────────────────────────────┐
                                    │         PUBLIC INTERNET           │
                                    └─────────────────┬─────────────────┘
                                                      │ HTTPS (:443) / SMTP (:25, :587)
                                                      ▼
                                    ┌───────────────────────────────────┐
                                    │      NGINX REVERSE PROXY          │
                                    │     (antifatypes.com SSL)         │
                                    └─────────┬───────────────┬─────────┘
                                              │               │
                        ┌─────────────────────┴──────┐        └─────────────────────┐
                        ▼                            ▼                              ▼
          ┌───────────────────────────┐┌───────────────────────────┐  ┌───────────────────────────┐
          │  FASTAPI CONTROL PLANE    ││   ADMIN WORKSTATION UI    │  │    SELF-HOSTED POSTFIX    │
          │      (Port :8444)         ││     (/admin/ /app/)       │  │     & DOVECOT IMAP        │
          └─────────────┬─────────────┘└─────────────┬─────────────┘  └─────────────┬─────────────┘
                        │                            │                              │
         ┌──────────────┴──────────────┐             │                              │
         ▼                             ▼             │                              ▼
┌─────────────────┐           ┌─────────────────┐    │                 ┌──────────────────────────┐
│ POSTGRESQL 14   │           │ AI WORKER ENGINE│◄───┘                 │  OCI EMAIL DELIVERY ZRH  │
│ (RLS Isolation) │           │   (Port :9000)  │                      │ (SPF, DKIM, DMARC Relay) │
└─────────────────┘           └────────┬────────┘                      └──────────────────────────┘
                                       │ Tool Execution
                     ┌─────────────────┼─────────────────┐
                     ▼                 ▼                 ▼
             ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
             │ Isolated Disk │ │ Code Exec     │ │ OpenRouter    │
             │ Workspaces    │ │ Python Sandbox│ │ Multi-LLM     │
             └───────────────┘ └───────────────┘ └───────────────┘
```

---

## 2. Core Subsystems & Network Topology

### A. Control Plane (`:8444`)
- **Technology**: FastAPI 0.110+, Python 3.11, Uvicorn, asyncpg.
- **Responsibilities**:
  * Multi-tenant authentication, session management, HMAC signature verification.
  * Row-Level Security (RLS) context injection per request.
  * REST API routing for Threads, Memories, Skills, Artifacts, Rubrics, Live Mode, Waitlist, and Mail.
  * Telegram webhook reception and callback dispatching.

### B. AI Worker Runtime Engine (`:9000`)
- **Technology**: FastAPI, Asyncio, Tool Registry, ReAct Loop.
- **Skills Active (15 Total)**:
  * `web_search`: DuckDuckGo / Tavily / Serper real-time web intelligence.
  * `code_exec`: Sandboxed Python execution with timeout and output capture.
  * `file_ops`: Per-tenant workspace filesystem manipulation.
  * `browser`: Headless web browsing and DOM extraction.
  * `website_builder`: Generates modern Tailwind CSS / HTML5 web apps and publishes them edge-ready under `/s/{slug}`.
  * `doc_builder`: Generates AES-256-GCM zero-knowledge encrypted executive documents and proposals under `/d/{slug}`.
  * `email_ops`: Autonomous bidirectional email handling (`send`, `inbox`, `read`, `reply`).
  * `memory_save`: Auto-persists standing facts, user preferences, and project rules.
  * `data_analysis`, `planner`, `image_gen`, `text_to_speech`, `api_caller`, `dorotheum_valuation`, `email_sender`.

### C. Self-Hosted & OCI Email Infrastructure
- **Local Daemons**:
  * Postfix 3.5.8 (Port 25/587) with SASL authentication.
  * Dovecot 2.3.16 (IMAP 993/143) with Maildir storage at `/home/opc/Maildir/`.
- **Authenticated Relay**:
  * Oracle Cloud Infrastructure Email Delivery (Zurich `eu-zurich-1`, port 587).
  * SPF: `v=spf1 ip4:132.226.223.180 include:eu.rp.oracleemaildelivery.com ~all`
  * DKIM: `ironclaw._domainkey` CNAME to `ironclaw.antifatypes.com.dkim.zrh1.oracleemaildelivery.com`.
  * DMARC: `v=DMARC1; p=none; sp=none`.

### D. AI Watchdog Guardian (`ironclaw-watchdog.service`)
- **Mode**: 100% Deterministic & Silent Auto-Healing (0 LLM tokens, 0 spam).
- **Function**: Probes localhost ports `:8444`, `:9000`, `:5432`, `:443`, `:25` every 60 seconds; auto-restarts failed services via `systemctl restart`; writes live hardware telemetry to `guardian_status.json`; dispatches Telegram alerts **only** on actual outage and recovery events.
