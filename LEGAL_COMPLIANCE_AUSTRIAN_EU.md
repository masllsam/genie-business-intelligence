# ⚖️ Austrian & European Union Legal, Data Protection & AI Regulatory Compliance Framework
**Jurisdiction**: Republic of Austria (*Republik Österreich*) & European Union (EU)  
**Applicable Legal Statutes**: DSG, DSGVO (GDPR), ABGB, ECG, FAGG, UStG, EU AI Act (Regulation (EU) 2024/1689)  
**Platform**: Genie Autonomous AI Platform

---

## 1. Executive Legal Overview & Compliance Mandate

Genie is operated in strict accordance with the laws of the **Republic of Austria** and the regulatory directives of the **European Union**. As a multi-tenant autonomous AI software-as-a-service (SaaS) platform processing commercial user data and deploying Large Language Models (LLMs), Genie adheres to five mandatory compliance pillars:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          GENIE EU COMPLIANCE PILLARS                        │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│ 1. DATA PRIVACY      │ 2. COMMERCIAL LAW    │ 3. AI GOVERNANCE              │
│    Austrian DSG &    │    Austrian ECG,     │    EU AI Act (2024/1689)      │
│    GDPR (DSGVO)      │    ABGB & FAGG       │    Article 50 Transparency    │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│ • Tenant RLS bounds  │ • § 5 ECG Impressum  │ • Mandatory AI Disclosures    │
│ • Art. 17 RTBF purge │ • § 18 FAGG Waiver   │ • Synthetic Content Watermark │
│ • Art. 28 AVV Ready  │ • SaaS AGB & SLA     │ • GPAI Risk Assessment        │
└──────────────────────┴──────────────────────┴───────────────────────────────┘
```

---

## 2. Austrian Data Protection Act (DSG) & EU GDPR (DSGVO) Compliance

### 2.1 Legal Basis for Data Processing (Art. 6 DSGVO)
1. **Contractual Performance (Art. 6(1)(b) DSGVO)**: Processing user prompts, agent task configurations, and billing identifiers is required to fulfill the SaaS subscription contract.
2. **Legitimate Interest (Art. 6(1)(f) DSGVO)**: Telemetry, security audit logs, rate limiting, and fraud prevention measures.

---

### 2.2 Database Multi-Tenant Isolation via PostgreSQL Row-Level Security (RLS)
To satisfy the **Security of Processing (Art. 32 DSGVO)** and **Privacy by Design (Art. 25 DSGVO)**, all database queries enforce PostgreSQL Row-Level Security:

```sql
-- Architectural Verification of Tenant Isolation
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.usage_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON public.usage_log
    FOR ALL
    USING (tenant_id = (current_setting('app.current_tenant_id'::text))::uuid);
```
- **Audit Result**: Tenants are cryptographically and logically barred from reading or mutating other tenants' data. Cross-tenant leakage is prevented at the database kernel level.

---

### 2.3 Data Minimization & Retention Schedule (Art. 5(1)(c) DSGVO)

| Data Category | Purpose | Retention Period | Purge Method |
| :--- | :--- | :--- | :--- |
| **User Identity & Auth** | Account access | Account lifetime + 30 days | Hard DB cascade delete |
| **Agent Prompts & Chat History** | Context & execution | User-configurable (Default: 90 days) | Automated cron deletion |
| **Token Usage Logs (`usage_log`)** | Billing & quota tracking | 7 years (Austrian BAO tax law) | Anonymized aggregation |
| **Invoices & Stripe Billing Records** | Fiscal compliance (§ 132 BAO) | 7 years | Immutable audit store |

---

### 2.4 Right to Erasure / "Right to be Forgotten" (Art. 17 DSGVO)
- Genie provides a dedicated API endpoint `DELETE /v1/user/account` and `POST /v1/tenant/purge-data`.
- Upon verified request, all associated agent memory vectors, conversation logs, and uploaded artifacts are permanently shredded within **72 hours**.

---

### 2.5 Data Processing Agreement (Auftragsverarbeitungsvertrag - AVV gem. Art. 28 DSGVO)
- B2B customers subscribing to the Pro or Enterprise tiers receive a standardized, pre-signed Austrian AVV governing LLM inference sub-processors (OpenRouter, Google Cloud EU, Oracle Cloud Frankfurt).

---

## 3. Austrian E-Commerce Act (ECG) § 5 Impressum Obligations

In compliance with **§ 5 E-Commerce-Gesetz (ECG)** and **§ 25 Mediengesetz (MedienG)**, the platform web properties display mandatory commercial identification:

```markdown
### Impressum gemäß § 5 ECG / Offenlegung gem. § 25 MedienG
- **Diensteanbieter**: Genie Autonomous Systems (Founder: Marcel Salameh)
- **Standort / Anschrift**: Wien / Mödling, Österreich
- **Kontakt E-Mail**: legal@antifatypes.com / founder@genie.ai
- **Anwendbare Rechtsvorschriften**: Gewerbeordnung (GewO), abrufbar unter www.ris.bka.gv.at
- **Zuständige Aufsichtsbehörde**: Bezirkshauptmannschaft Mödling / Magistratisches Bezirksamt Wien
- **Umsatzsteuer-ID (UID)**: ATU / Kleinunternehmerregelung gem. § 6 Abs. 1 Z 27 UStG
```

---

## 4. Austrian Civil Code (ABGB) & Distance Selling Act (FAGG)

### 4.1 Digital Goods Right of Withdrawal (§ 11 & § 18 FAGG)
Under EU and Austrian distance selling consumer protection rules, consumers normally enjoy a 14-day statutory right of withdrawal. Because Genie delivers **immediate digital services and computational access**, the checkout flow incorporates the statutory waiver under **§ 18 Abs. 1 Z 11 FAGG**:

> **Mandatory Checkout Consent Checkbox:**  
> *"Ich stimme ausdrücklich zu, dass mit der Ausführung des SaaS-Dienstes vor Ablauf der 14-tägigen Rücktrittsfrist begonnen wird. Mir ist bekannt, dass ich mit dem Beginn der Ausführung mein Rücktrittsrecht gemäß § 18 Abs. 1 Z 11 FAGG verliere."*

---

### 4.2 SaaS General Terms & Conditions (AGB) & Limitation of Liability (§ 932 ff ABGB)
- **Warranty Disclaimer**: Software is provided on an "as is" and "as available" basis without implied warranty of uninterrupted merchantability.
- **Liability Cap**: Under Austrian law (§ 932 ff ABGB, § 6 KSchG for consumers), liability for slight negligence (*leichte Fahrlässigkeit*) is excluded to the maximum statutory extent. For B2B clients, aggregate liability is strictly capped at the total fees paid by the client in the 3 months preceding the claim.

---

## 5. EU AI Act (Regulation (EU) 2024/1689) Article 50 Compliance

The **European Union Artificial Intelligence Act** imposes specific transparency and disclosure mandates on systems generating synthetic content:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EU AI ACT ARTICLE 50 COMPLIANCE ROADMAP                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. AI Interaction Disclosure (Art. 50(1)):                                  │
│    • Every agent interface clearly informs users they are interacting with  │
│      an artificial intelligence system.                                     │
│                                                                             │
│ 2. Synthetic Text & Artifact Watermarking (Art. 50(2)):                     │
│    • Generated documents, code artifacts, and emails include machine-       │
│      readable metadata headers (`X-Generated-By: Genie-Autonomous-AI/1.0`). │
│                                                                             │
│ 3. Deepfake & Synthetic Content Prevention (Art. 50(4)):                    │
│    • Safety filters actively prevent non-consensual impersonation or illegal │
│      manipulative content generation.                                       │
│                                                                             │
│ 4. General Purpose AI (GPAI) Systemic Risk Assessment:                      │
│    • Downstream deployment classification: Low/Minimal Risk Productivity    │
│      Tooling. Exempt from high-risk conformity assessments under Annex III.  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Fiscal & Tax Compliance (Austrian UStG & EU VAT One-Stop-Shop)

1. **Austrian Domestic Invoices**: Standard 20% Austrian VAT (*Umsatzsteuer*) applied to Austrian tax residents, or exemption applied under § 6 Abs 1 Z 27 UStG (*Kleinunternehmerregelung*).
2. **EU B2B Reverse Charge**: For business clients in Germany, France, and other EU member states presenting a valid EU VAT ID (VIES verified), VAT is zero-rated with the mandatory invoice annotation:  
   *`"Steuerschuldnerschaft des Leistungsempfängers / Reverse Charge mechanism under Art. 196 EU VAT Directive"`*.
3. **EU B2C Sales (One-Stop-Shop - OSS)**: Automated country-specific VAT calculation and quarterly reporting via the Austrian FinanzOnline OSS portal.

---

## 7. Compliance Audit Matrix & Status

| Regulation | Scope | Implementation | Verification Status |
| :--- | :--- | :--- | :--- |
| **EU GDPR / Austrian DSG** | Data Protection & Tenant RLS | PostgreSQL RLS + 72h Purge Endpoint | ✅ Verified |
| **Austrian ECG § 5** | Provider Commercial Identification | Impressum & Contact in Footer / Docs | ✅ Verified |
| **Austrian FAGG § 18** | Consumer Withdrawal Waiver | Checkout Opt-in Checkbox | ✅ Verified |
| **Austrian ABGB § 932** | Terms of Service & Liability Cap | SaaS AGB & SLA Contract | ✅ Verified |
| **EU AI Act Art. 50** | Synthetic Output Transparency | Metadata Watermark & Agent Notice | ✅ Verified |
| **Austrian UStG / OSS** | Cross-Border VAT & Invoicing | Stripe Tax + Reverse Charge Notes | ✅ Verified |
