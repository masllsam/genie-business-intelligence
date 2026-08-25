# 🛡️ NEAR AI IronClaw & HyperAgent Sovereign Architecture Alignment

## 1. The Lineage: From `nearai/ironclaw` to the Sovereign Telegram Fleet

The **IronClaw** project originates from the core architectural philosophy of **NEAR AI's IronClaw (`nearai/ironclaw`)**: a security-first, capability-based Agent OS designed as a sovereign, privacy-preserving alternative to bloated big-tech agent wrappers.

### Core NEAR AI IronClaw Principles Embedded in Our Platform:
1. **Data Sovereignty & Local Encryption**:
   - Tenant data is strictly isolated using PostgreSQL 14 Row-Level Security (RLS) with null-safe parameter boundaries.
   - User artifacts (proposals, sites, records) are encrypted using **WebCrypto AES-256-GCM** client-side encryption.
2. **Capability-Based Tool Execution & Sandboxing**:
   - The worker runtime (`:9000`) isolates tool execution into discrete capability modules (`code_exec` in sandboxed Python, `file_ops` confined to `/workspaces/{tenant_id}`, `website_builder` outputting isolated unguessable `/s/site_{token}/` paths).
   - Sensitive credentials (`OPENROUTER_API_KEY`, `WORKER_SECRET`, Stripe live tokens) are kept strictly in backend environment stores, never reflected into LLM prompt contexts.
3. **Multi-Tier Privacy & Offline Resilience**:
   - Primary LLM routing via OpenRouter / Gemini 3.7 Flash with an automatic **100% local, air-gapped fallback pool** running on local Ollama instances (`llama3.2:1b`, `qwen2.5-coder:3b`) on the Oracle ARM64 host.

---

## 2. The HyperAgent Stateful Synthesis

To eliminate token context bloat and agent amnesia, we synthesized **HyperAgent's core paradigms**:

| HyperAgent Concept | IronClaw / Genie Implementation |
| :--- | :--- |
| **Thread Context Document (TCD)** | A living markdown state document maintaining current project objectives, completed steps, and open action items without dumping raw message history into prompts. |
| **Dynamic Memory Graph** | Fact & rule storage scored on an **Importance 1–5 scale**. Importance 4–5 memories are pinned globally; Importance 1–3 memories are surfaced dynamically via trigger keywords. |
| **Autonomous Watchers** | Background daemons (`live_mode_watchers`) that continuously probe URLs, APIs, or telemetry and proactively dispatch briefings over Telegram. |
| **Evaluative Rubrics** | Automated output scoring against multi-dimensional criteria (accuracy, clarity, format, tone). |

---

## 3. The Universal Reachability Moat: "Just a Phone"

While `nearai/ironclaw` focuses on desktop shells (Tauri) and CLI tools, our implementation bridges this capability to **any phone on Earth**:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   NEAR AI IRONCLAW + TELEGRAM EDGE BRIDGE                        │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   [ 📱 Telegram Chat ]        [ 📱 Telegram Mini App ]    [ 📻 LoRa Radio / SMS ]│
│    (Plain text / Voice)          (Cyber-Dark Console)      (128-byte raw packet) │
│            │                             │                           │           │
│            └─────────────────────────────┼───────────────────────────┘           │
│                                          ▼                                       │
│                       ┌─────────────────────────────────────┐                    │
│                       │   DISPATCHER (HMAC & Route Guard)   │                    │
│                       │   `POST /webhook/{webhook_id}`      │                    │
│                       │   (X-Worker-Token: WORKER_SECRET)   │                    │
│                       └──────────────────┬──────────────────┘                    │
│                                          │                                       │
│                                          ▼                                       │
│                       ┌─────────────────────────────────────┐                    │
│                       │   NEAR AI IRONCLAW WORKER RUNTIME   │                    │
│                       │   • HyperAgent Dynamic Memory Graph │                    │
│                       │   • Sandboxed ReAct Tool Loop (15)  │                    │
│                       │   • Air-Gap Ollama Fallback Pool    │                    │
│                       └──────────────────┬──────────────────┘                    │
│                                          │                                       │
│                                          ▼                                       │
│                       ┌─────────────────────────────────────┐                    │
│                       │   SOVEREIGN ARTIFACT GENERATION     │                    │
│                       │   • /s/ Live Responsive Websites    │                    │
│                       │   • /d/ WebCrypto Encrypted Docs    │                    │
│                       │   • Sandboxed Python Output         │                    │
│                       └─────────────────────────────────────┘                    │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Current Platform State & Version Tracking

- **Git Version Tag**: [`v1.2.0-stable`](https://github.com/masllsam/ironclaw/releases/tag/v1.2.0-stable)
- **Test Suite Status**: **32/32 Passed (100.0%)** across all 8 platform test suites.
- **Active Daemons**: All 8 services (`control-plane`, `worker`, `dispatcher`, `watchdog`, `activity-keeper`, `nginx`, `postgresql`, `ollama`) running live.
- **Telegram Bot**: Fully active on `@l40l4bot` with zero worker errors.
