# Sovereign Artifact Ownership, Code Extraction & Autonomous Multi-Rail Deployment

## 1. Executive Summary & Problem Statement

In conventional AI assistant workflows, generated artifacts (e.g., websites, documents, scripts, notebooks, datasets) are trapped in closed platform silos. The user can view a rendered output on the host domain (e.g. `https://antifatypes.com/s/...`), but cannot easily:
1. **Own the Raw Code**: Inspect syntax, edit markup, or review dependencies.
2. **Download Standalone Bundles**: Obtain a self-contained `.zip` package with zero runtime dependencies.
3. **Deploy to Their Own Webspace**: Automatically push the code to GitHub Pages, Vercel, Cloudflare Pages, AWS S3, or self-hosted cPanel/Apache/Nginx webservers via webhooks.

This document establishes the architectural foundation for **100% User Code Sovereignty** within Genie / IronClaw, synthesizing the state-of-the-art approaches of **`nearai/ironclaw`**, **NearAI**, and **HyperAgent**.

---

## 2. Comparative Analysis: How Leading Systems Solve Artifact Ownership

| Dimension | `nearai/ironclaw` | NearAI | HyperAgent | Genie / Sovereign IronClaw |
| :--- | :--- | :--- | :--- | :--- |
| **Workspace Model** | Sandboxed tenant file trees with cryptographic process journaling | Immutable versioned hub registry (models/agents/data) | Dynamic Thread Context Documents with live artifact bridges | Sandboxed file workspaces with Row-Level Security (RLS) & WebCrypto encryption |
| **Code Inspection** | Direct raw file reads (`/workspace/files`) | Git-native branch explorer | Real-time code/diff viewer with syntax highlighting | In-browser Cyber-Dark Code Inspector (`/s/{slug}/code`) + copy/edit preview |
| **Download Pipeline** | Tarball workspace dump | Package source archive (`.tar.gz`) | Standalone `.zip` with manifest | 1-Click ZIP (`/s/{slug}/download`), raw `.html`/`.md` download, and native Telegram file delivery (`sendDocument`) |
| **Deployment Rails** | OCI runner process dispatch | Automated GitHub Actions CI/CD workflows | Webhook dispatch & CNAME custom domain pointers | **Multi-Rail Deployment Hub**:<br>1. 1-Click GitHub Pages push<br>2. Signed Webhook dispatch (cPanel/WordPress/S3)<br>3. DNS CNAME custom domains |

---

## 3. Architecture Specification

### 3.1 Standardized Artifact Bundle Specification
Every generated website or web application is compiled into a standalone directory on disk (`/home/opc/ironclaw/sites/{site_id}/`) structured as:
```text
site_30523486c45293ae0b562632/
├── index.html            # Standalone, responsive HTML5/Tailwind/Alpine.js application
├── README.md             # Project overview, customization instructions, and deployment guide
├── metadata.json         # Cryptographic SHA-256 hash, creation timestamp, theme, and tags
├── CNAME                 # Optional custom domain configuration
└── assets/               # Local static assets, icons, and stylesheets (if applicable)
```

### 3.2 Universal HTTP Endpoints

#### 1. Instant ZIP Bundle Download
* **Route**: `GET /s/{slug}/download`
* **Response**: `Content-Type: application/zip`, `Content-Disposition: attachment; filename="{slug}.zip"`
* **Behavior**: Dynamically zips the folder in memory and streams it directly to the user with zero latency.

#### 2. In-Browser Code Inspector
* **Route**: `GET /s/{slug}/code`
* **Response**: A high-performance Cyber-Dark code viewer featuring:
  - Line numbering & syntax highlighting.
  - 1-Click "Copy Raw HTML" button.
  - "Download Standalone Bundle" button.
  - Live Side-by-Side Preview toggle.

#### 3. Cryptographic Document & Script Extraction
* **Route**: `GET /d/{slug}/download`
* **Response**: Dual export options:
  - `?format=md`: Pure unencrypted Markdown source.
  - `?format=html`: Standalone print-ready WebCrypto decryptor page for offline archival.

#### 4. Multi-Rail Webspace Deployer
* **Route**: `POST /api/v1/artifacts/{id}/deploy`
* **Payload**:
  ```json
  {
    "provider": "github" | "webhook" | "cname",
    "github_token": "ghp_...",
    "github_repo": "username/my-watch-site",
    "webhook_url": "https://myserver.com/api/deploy-receiver",
    "webhook_secret": "whsec_...",
    "custom_domain": "watches.mybrand.com"
  }
  ```

---

## 4. Multi-Rail Deployment Playbooks

### Rail 1: Deploy to GitHub Pages (1-Click)
1. The platform initializes a git tree with `index.html` and `README.md`.
2. Authenticates via user's GitHub Personal Access Token or OAuth.
3. Creates or updates the target repository and commits to the `gh-pages` branch.
4. Returns the live GitHub Pages URL (e.g., `https://username.github.io/my-watch-site/`).

### Rail 2: Deploy to Vercel / Netlify / Cloudflare Pages
Users can simply connect their GitHub repository or drag-and-drop the downloaded `.zip` file into the Vercel/Netlify dashboard for instant global edge CDN hosting.

### Rail 3: Deploy to Self-Hosted Webspace (cPanel / Apache / Nginx / Webhook)
For users running their own VPS or shared hosting:
1. User enters their deployment webhook URL in the Web Console or Telegram.
2. Platform sends a cryptographic `POST` request containing the base64-encoded zip bundle and SHA-256 HMAC signature.
3. User's lightweight drop script unpacks the bundle into `/var/www/html/` automatically.

---

## 5. Security & Privacy Guarantees
* **Zero Host Lock-in**: All code is 100% self-contained standard HTML5/CSS/JS without proprietary host scripts.
* **Isolated Namespaces**: Artifacts are mapped to strict tenant UUIDs with Row-Level Security.
* **Encrypted Archives**: Private documents remain end-to-end encrypted with AES-GCM-256.
