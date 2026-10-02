---
type: Overview
title: "Knowledge Guide Starter Template (Google OKF v0.2)"
description: "A turnkey, self-contained, and self-maintaining knowledge base template for engineering, product, and operational teams."
tags: [readme, overview, template, okf, llm-wiki, agentic-docs]
status: stable
generated:
  by: agent:antigravity
  at: 2026-09-26T00:00:00Z
verified:
  - by: human:architecture-lead
    at: 2026-09-26T00:00:00Z
---

# Knowledge Guide Starter Template (Google OKF v0.2)

A production-grade, turnkey template for creating a **self-contained, self-healing, and self-maintaining knowledge base** for any organization. Adheres strictly to the **Google Cloud Open Knowledge Format (OKF v0.2)** standard.

Designed from the ground up for seamless collaboration between **human engineering teams** and **autonomous AI coding agents** (Antigravity, Claude Code, Cursor, Copilot, Cline, Aider, Devin).

---

## ⚡ Why This Knowledge Base Architecture Works

Traditional wikis (Confluence, Notion, Google Docs) fail for software teams because they drift from code, require proprietary sync pipelines, and confuse active reality with speculative proposals.

This template solves that by implementing the **Open Knowledge Format (OKF v0.2)** pattern:

1. **Zero External Dependencies**: Powered entirely by the Python 3 standard library and Git. No databases, vector stores, Node.js runtimes, or pip dependencies required.
2. **Self-Healing Presubmit Gatekeeper**: Git pre-commit and pre-push hooks automatically generate missing frontmatter, normalize statuses, fix broken relative links, synchronize `index.md`, and auto-stage repaired files.
3. **Architectural Demarcation**:
   * **"What Is"**: Operational reality, external regulations (`/ecosystem/`), and active production software (`/systems/`) with `status: stable`.
   * **"What Could Be"**: Future feature proposals and architectural RFCs (`/concepts/`) with `status: draft`.
   * **"How To" & Provenance**: Operational runbooks (`/playbooks/`), customer research (`/research/`), and standards (`/references/`).
4. **Progressive Disclosure**: Built for LLM context efficiency. Agents read [`index.md`](file:///index.md) first to scan categorized one-line summaries before traversing deep files.
5. **Living Agent Operating Contract**: Includes [`AGENTS.md`](file:///AGENTS.md) at repository root to govern autonomous AI agent interactions, non-negotiable compliance rules, and ground truth resolution.
6. **Turnkey AI Agent Skills**: Ships with built-in agent capabilities:
   * **`ask-kb`**: Instant architectural and domain consulting (`/ask-kb <query>` or CLI `python3 scripts/query_kb.py "<query>"`).
   * **`manage-knowledge-base`**: Standardized protocols for AI agents to navigate, author, update, and audit knowledge.
   * **`ingest`**: Command any AI agent to `ingest <URL>`—it fetches the page, consults with you on placement, formats an OKF v0.2 document, and validates the bundle.

---

## 🚀 Quickstart: Setting Up a New Organization in 30 Seconds

### 1. Clone or Template
Clone this repository to your machine or workspace:
```bash
git clone <repository_url> my-org-guide
cd my-org-guide
```

### 2. Personalize / Brand for Your Organization
Run the single-command branding script:
```bash
./init.sh --org "Acme Health" --title "Acme Knowledge Base"
```
*(Interactively prompts for details if arguments are omitted. Configures `knowledge.config.json`, updates headers, rebuilds the index, and validates.)*

### 3. Run Automated Environment Setup
Installs Git presubmit hooks, verifies permissions, registers agent discovery, and runs self-test validation:
```bash
./setup.sh
```

---

## 🧭 Repository Structure

```text
knowledge-guide/
├── index.md                 # Root OKF index (progressive disclosure entry point)
├── log.md                   # Chronological update history (ISO 8601 YYYY-MM-DD)
├── AGENTS.md                # AI Agent Guidelines & Operating Contract
├── knowledge.config.json    # Organization name, title, and category mappings
├── init.sh                  # Interactive organization customizer
├── setup.sh                 # Environment setup and Git presubmit hook installer
├── SETUP.md                 # Autonomous AI agent and human onboarding runbook
│
├── 🏛️ ecosystem/            # "WHAT IS" - External Reality, Regulators & Partner Rails
│   └── industry-landscape.md
│
├── 💻 systems/              # "WHAT IS" - Active Production Architecture & Services
│   └── core-architecture.md
│
├── 💡 concepts/             # "WHAT COULD BE" - Feature Proposals & Architectural RFCs
│   └── future-initiative.md
│
├── 📋 playbooks/            # Operational Runbooks, Setup Guides & SOPs
│   ├── onboarding-guide.md
│   ├── knowledge-driven-engineering.md
│   └── generating-product-storyboards.md
│
├── 🎙️ research/             # Customer Interviews, Field Observations & User Research
│   └── user-interview-example.md
│
├── 📖 references/           # Specifications, Schemas, Lineage & Standards
│   ├── okf-specification.md
│   └── provenance.md
│
├── 🛠️ scripts/              # Self-contained Python stdlib maintenance tools
│   ├── init_repo.py         # Org customizer / parameterizer
│   ├── presubmit.py         # Pre-commit & pre-push hook gatekeeper
│   ├── update_index.py      # Dynamic category-aware index generator
│   ├── query_kb.py          # Fast CLI keyword & relevance search tool
│   └── validate.py          # OKF v0.2 schema, link & trust tier validator
│
├── 🤖 skills/               # Reusable AI Agent Skills (.agents/skills)
│   ├── ask-kb/
│   │   ├── SKILL.md         # /ask-kb instant domain & architectural consulting
│   │   └── scripts/         # query_kb.py search tool
│   ├── manage-knowledge-base/
│   │   ├── SKILL.md         # Instructions for AI agents managing the repository
│   │   ├── references/      # OKF quick-reference cheat sheet
│   │   └── templates/       # Skill templates
│   ├── ingest/
│   │   ├── SKILL.md         # Instructions for ingesting external URLs
│   │   ├── scripts/         # Lightweight urllib/html.parser fetcher
│   │   └── templates/       # Ingested source template
│   └── generate-storyboards/
│       ├── SKILL.md         # Visual narrative storyboards for product concepts
│       ├── scripts/         # DOCX & HTML export script
│       └── templates/       # Storyboard document template
│
├── 🧩 templates/            # Authoring starter templates
│   ├── concept-template.md
│   ├── ecosystem-template.md
│   ├── playbook-template.md
│   ├── reference-template.md
│   ├── research-template.md
│   ├── storyboard-template.md
│   └── system-template.md
│
└── 🔮 .obsidian/            # Pre-configured Obsidian vault settings (Graph view)
```

---

## 🛠️ Maintenance Commands

All tools are standalone and require only standard Python 3.8+:

```bash
# 1. Run Presubmit Gatekeeper (auto-repairs frontmatter/links, rebuilds index, validates)
./scripts/presubmit.py

# 2. Search Knowledge Base via CLI
python3 scripts/query_kb.py "caching architecture"

# 3. Run Validator directly (with --fix to auto-repair issues)
python3 scripts/validate.py --fix

# 4. Synchronize Root index.md from all concept files
python3 scripts/update_index.py

# 5. Ingest external documentation via AI agent
# In chat: "ingest https://example.com/api-spec"
```

---

## 📝 OKF v0.2 Frontmatter Contract

Every document in the knowledge base (except `log.md` and subdirectory `index.md`) begins with standard YAML frontmatter:

```yaml
---
type: System Component       # REQUIRED: e.g. Concept, Playbook, System Component
title: "Service Architecture" # Recommended: Human-readable title
description: "One-line summary for progressive disclosure index."
tags: [architecture, backend] # Optional: Tag list
status: stable               # Optional: draft | stable | deprecated (default: stable)
stale_after: 2027-01-01T00:00:00Z # Optional: Expiration threshold
generated:                   # Optional: Production metadata
  by: agent:antigravity
  at: 2026-09-26T00:00:00Z
verified:                    # Optional: Trust and audit events
  - by: human:architecture-lead
    at: 2026-09-26T00:00:00Z
sources:                     # Optional: Provenance citations
  - id: source:github-repo
    resource: https://github.com/my-org/my-service
    title: "Production Service Repository"
---
```

---

## 🌐 Obsidian Integration

This repository is ready to open directly in [Obsidian](https://obsidian.md/):
* `.obsidian/app.json` is configured for standard markdown links (`useMarkdownLinks: true`).
* `.obsidian/community-plugins.json` is configured for `obsidian-git` auto-sync.
* Interactive graph view visualizes cross-references between `/systems/`, `/ecosystem/`, and `/concepts/` out of the box.

---

## 📜 Specification & License

* Conforms to the [Google Cloud Open Knowledge Format (OKF v0.2)](https://github.com/GoogleCloudPlatform/open-knowledge-format).
* Freely reusable and distributable under Apache 2.0 / MIT.
