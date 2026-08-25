# IronClaw Platform: Legal & Regulatory Compliance Specification

## 1. Compliance Architecture Overview

Operating an autonomous multi-tenant AI agent SaaS platform in 2026 requires adherence to multi-jurisdictional standards:
1. **European Union AI Act (Regulation EU 2024/1689)**
2. **General Data Protection Regulation (GDPR - Regulation EU 2016/679)**
3. **Swiss Federal Act on Data Protection (FADP / DSG)**
4. **German Digital Services Act (§ 5 DDG / TMG)**
5. **ePrivacy Directive & CAN-SPAM Act**

---

## 2. EU AI Act (2024/1689) Risk Classification & Obligations

### A. Risk Categorization: **Minimal to Limited Risk AI System**
IronClaw functions as an autonomous general-purpose agent orchestration platform executing sandboxed user instructions (code writing, document synthesis, web analysis). It does **not** perform prohibited AI practices (biometric identification, cognitive behavioral manipulation, social scoring) nor does it deploy safety-critical medical/infrastructure high-risk models.

### B. Transparency Obligations (Article 50 Compliance):
- **User Disclosure**: Clear disclosure across all interfaces (`/`, `/app/`, `/d/`) that outputs are AI-generated.
- **AI Disclaimer**: Explicit disclaimers stating that generated code, legal proposals, market analyses, and financial valuations do **not** constitute certified professional advice.
- **Watermarking & Provenance**: Encrypted documents (`/d/{slug}`) and sites (`/s/{slug}`) include metadata headers identifying agent orchestration.

---

## 3. GDPR & Swiss FADP Data Protection Compliance

| Requirement | Implementation in IronClaw | Legal Reference |
| :--- | :--- | :--- |
| **Lawfulness of Processing** | Processing based on Contract (Art. 6(1)(b)) and Consent (Art. 6(1)(a)). | GDPR Art. 6 |
| **Data Minimization** | No third-party ad tracking, no unnecessary telemetry collection. | GDPR Art. 5(1)(c) |
| **Tenant Data Isolation** | PostgreSQL Row-Level Security (RLS) guarantees complete cryptographic separation of tenant memories and workspaces. | GDPR Art. 32 |
| **Zero-Knowledge Encryption** | Client proposals (`/d/...`) use PBKDF2 (100k) + AES-256-GCM. Passphrases never touch servers. | GDPR Art. 32 (State of the Art) |
| **Right to Erasure** | Users can delete waitlist records and tenant workspaces with instant cascade deletion. | GDPR Art. 17 |
| **Cross-Border Transfers** | Hosted on Oracle Cloud EU/Zurich/Frankfurt data centers with Zero Data Retention (ZDR) on LLM inference pipelines. | GDPR Chapter V |

---

## 4. Anti-Spam & Transactional Email Compliance

- **Double Opt-In**: Waitlist subscribers receive transactional verification emails before priority queue activation.
- **Sender Identification**: All outbound emails identify `noreply@antifatypes.com` with reverse DNS, SPF (`eu.rp.oracleemaildelivery.com`), DKIM (`ironclaw._domainkey`), and DMARC (`v=DMARC1; p=none; sp=none`).
- **Unsubscribe Mechanism**: Plaintext and HTML email footers include instant unsubscribe links and physical legal contact details.

---

## 5. Live Legal Endpoints on `antifatypes.com`

- **Privacy Policy**: `https://antifatypes.com/privacy.html`
- **Terms of Service & Acceptable Use**: `https://antifatypes.com/terms.html`
- **Legal Notice & Impressum**: `https://antifatypes.com/legal.html`
- **Data Protection Inquiries**: `privacy@antifatypes.com`
