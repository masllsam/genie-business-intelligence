# HyperAgent Reverse-Engineered Architecture & Features Guide

## 1. Feature Parity Matrix

| HyperAgent Concept | IronClaw Implementation | Database Table | API Endpoint Prefix | Worker Skill |
| :--- | :--- | :--- | :--- | :--- |
| **Persistent Threads** | Persistent Conversation Workspaces | `threads`, `thread_messages` | `/api/v1/threads` | Context Assembler |
| **Thread Context Doc** | Dynamic Markdown TCD | `threads.thread_context_doc` | `PATCH /threads/{id}/context` | Auto-Summarizer |
| **Standing Memories** | Priority 4-5 Core Facts | `memories` (importance 4-5) | `/api/v1/memories` | Always-Include Injector |
| **Dynamic Memories** | Keyword & Tag Surfaced Facts | `memories` (importance 1-3) | `GET /memories/search` | `memory_save` Skill |
| **Composable Skills** | Frontmatter YAML + Markdown | `skills` | `/api/v1/skills` | Skill Registry |
| **Pinned Skills** | Persistent Execution Instructions | `skills.is_pinned = TRUE` | `POST /skills/{id}/pin` | System Prompt Injector |
| **Unified Artifacts** | Published Web & Docs Engine | `artifacts` | `/api/v1/artifacts` | `website_builder`, `doc_builder` |
| **Zero-Knowledge AES** | Client-Side Password Crypto | `artifacts.is_encrypted` | `/d/{slug}` viewer | PBKDF2 + AES-256-GCM |
| **Automated Rubrics** | Multi-Criteria LLM Evaluator | `rubrics`, `evaluations` | `/api/v1/rubrics` | Evaluation Engine |
| **Live Mode Watchers** | Autonomous URL Change Daemon | `live_mode_watchers` | `/api/v1/live-mode` | `live_mode_daemon.py` |

---

## 2. Deep Dive: Architectural Concepts

### A. Persistent Threads & Thread Context Documents (TCD)
In IronClaw, conversations are not ephemeral message arrays. Every thread maintains a living **Thread Context Document (TCD)**:
- As agents and users converse, the TCD summarizes active objectives, established decisions, and completed milestones.
- When an agent turn executes, the current TCD is injected into the model context before previous message history, eliminating hallucination on long-running tasks.

### B. Two-Tier Memory Architecture
1. **Tier 1: Standing Memories (Importance 4–5)**:
   - High-priority operational rules, user preferences, and business constraints.
   - Automatically injected into the prompt of **every agent invocation** regardless of the user query.
2. **Tier 2: Dynamic Memories (Importance 1–3)**:
   - Factoids, past context, and reference datasets.
   - Surfaced dynamically based on keyword search and PostgreSQL text array tag matching (`tags && ARRAY['finance', 'europe']`).

### C. Composable Skills with YAML Frontmatter
Skills are defined in clean markdown with structured parameters:
```yaml
---
name: market_research
description: Deep market scanning and competitive matrix analysis.
parameters:
  query: { type: string, description: "Market sector to analyze" }
  depth: { type: integer, description: "Scan depth (1-5)" }
---
Instructions for the agent when executing this skill...
```
- Pinned skills are loaded verbatim into the system instructions.
- Unpinned skills are exposed as callable ReAct tools in the LLM tool-calling schema.

### D. Zero-Knowledge Encrypted Document Engine (`/d/{slug}`)
- Generates professional proposals, audit reports, and contracts.
- Uses **PBKDF2 (100,000 iterations)** with cryptographic salt and **AES-256-GCM** encryption.
- The decryption key is **never sent to the server**. Decryption happens 100% in the client browser using WebCrypto APIs.
- Instant Revocation Kill-Switch (`POST /api/v1/artifacts/{id}/revoke`).
