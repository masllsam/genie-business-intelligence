# AgentFleet: Third-Party Open Source Software Notices & Licenses

**Platform:** AgentFleet Autonomous Systems (`antifatypes.com`)  
**Date:** August 17, 2026  
**Compliance Standard:** Mandatory attribution under MIT, Apache 2.0, BSD-3-Clause, EPL-2.0, PostgreSQL License, and SIL OFL 1.1

---

## 1. Core API & Microservices (Python ASGI)

| Package | Version | License | Copyright Holder / Author | Usage Description |
| :--- | :--- | :--- | :--- | :--- |
| `fastapi` | `>=0.110` | MIT | Sebastián Ramírez | Primary multi-tenant API gateway and webhook router |
| `starlette` | `>=0.36` | BSD-3-Clause | Encode OSS Ltd | Request lifecycle, middleware pipeline, exception handling |
| `uvicorn` | `>=0.28` | BSD-3-Clause | Encode OSS Ltd | Lightning-fast ASGI production web server |
| `pydantic` | `>=2.6` | MIT | Samuel Colvin | Strict schema validation and settings parsing |
| `asyncpg` | `>=0.29` | Apache 2.0 | MagicStack Inc. | High-throughput asynchronous PostgreSQL connection pool |
| `httpx` | `>=0.27` | BSD-3-Clause | Encode OSS Ltd | Asynchronous HTTP client for skill executions |
| `cryptography` | `>=42.0` | Apache 2.0 / BSD | PyCA (Python Cryptographic Authority) | AES-256-GCM authenticated cipher primitives & token hashing |

---

## 2. AI Worker Engine & Skills Runtimes

| Package | License | Copyright Holder / Author | Usage Description |
| :--- | :--- | :--- | :--- |
| `pandas` | BSD-3-Clause | NumFOCUS / Pandas Team | Sandboxed dataset ingestion and statistical analysis |
| `numpy` | BSD-3-Clause | NumPy Developers | Numerical compute vector calculations |
| `beautifulsoup4` | MIT | Leonard Richardson | HTML DOM parsing and clean text extraction |
| `pyyaml` | MIT | Kirill Simonov | YAML frontmatter parsing for composable skill specs |
| `requests` | Apache 2.0 | Kenneth Reitz & Authors | Synchronous HTTP communication helpers |

---

## 3. Server Infrastructure & Edge Services

| Component | License | Project Lead / Maintainer | Usage Description |
| :--- | :--- | :--- | :--- |
| `PostgreSQL 14` | PostgreSQL License | PostgreSQL Global Dev Group | Multi-tenant relational storage with Row-Level Security |
| `Nginx` | 2-Clause BSD | Igor Sysoev / NGINX Inc. | Reverse proxy, SSL termination, edge static site caching |
| `Postfix MTA` | EPL-2.0 / IPL | Wietse Venema | Outbound transactional verification mail queue |
| `Dovecot` | MIT / LGPL-2.1 | Timo Sirainen | Inbound IMAP mailbox management |
| `Let's Encrypt / Certbot` | Apache 2.0 | Electronic Frontier Foundation (EFF) | Automated TLS 1.3 certificate provisioning |

---

## 4. Frontend Assets & Typography

| Framework / Asset | License | Copyright Holder | Usage Description |
| :--- | :--- | :--- | :--- |
| `Tailwind CSS` | MIT | Tailwind Labs Inc. | Utility CSS framework for generated client websites (`/s/...`) |
| `Geist & Geist Mono` | SIL OFL 1.1 | Vercel Inc. | Cyber-academic typography across landing and dashboards |
| `Telegram WebApp SDK` | Telegram Platform License | Telegram Messenger Inc. | Mobile bridge for the Telegram Console Mini App |
