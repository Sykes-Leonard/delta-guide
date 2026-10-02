---
name: ask-kb
type: Skill
title: "Knowledge Base Advisor (/ask-kb)"
description: "Provides instant, authoritative domain and architectural consulting across production systems, external ecosystems, and product concepts. Use when developers or AI agents need domain context, schema contracts, or compliance guidance."
status: stable
generated:
  by: agent:antigravity
  at: 2026-09-26T00:00:00Z
verified:
  - by: human:architecture-lead
    at: 2026-09-26T00:00:00Z
---

# Knowledge Base Advisor (`/ask-kb`)

## Overview

The **Knowledge Base Advisor** (`/ask-kb`) is an interactive and programmatic domain expert designed to assist software engineers, product managers, and autonomous AI coding agents working across the codebase.

It bridges the gap between software implementation (code, APIs, databases) and organizational reality (architecture invariants, regulatory compliance, external partner rails, and user research).

---

## 1. Slash Command & Activation

### Chat Slash Command
Type `/ask-kb` in the chat input box followed by your question:
```text
/ask-kb What is our caching strategy for high-throughput API endpoints?
/ask-kb What external regulatory constraints apply to customer data residency?
/ask-kb What are the required fields for our core service data contract?
```

### Automatic Agent Activation
AI agents should automatically activate this skill whenever:
* Answering questions about system architecture, data models, or external regulatory realities.
* Designing a new schema, UI component, background worker, or API endpoint.
* Conducting a pull request review for compliance, idempotency, or architectural alignment.

### CLI Query Tool
Developers and scripts can also run the bundled domain query CLI directly from the terminal:
```bash
# Query the knowledge base from CLI
python3 scripts/query_kb.py "api gateway auth"

# Filter by directory category (systems, ecosystem, concepts, playbooks)
python3 scripts/query_kb.py "data residency" --category ecosystem

# Output raw JSON for programmatic pipelines
python3 scripts/query_kb.py "queue" --json
```

---

## 2. Domain Knowledge Routing Matrix

When a query is received, consult the authoritative OKF documents across the repository:

| Domain Area | Key Questions Addressed | Authoritative KB Categories |
| :--- | :--- | :--- |
| **Production Systems** | Active services, schemas, tech stack, APIs, datastores | [`/systems/`](/systems/) |
| **External Ecosystem & Institutions** | Regulatory frameworks, partner APIs, statutory mandates, frontier labs, research institutes, moral authorities | [`/ecosystem/`](/ecosystem/), [`/ecosystem/institutions/`](/ecosystem/institutions/overview.md) |
| **Product Concepts** | Proposed features, architectural RFCs, exploratory initiatives | [`/concepts/`](/concepts/) |
| **Operational SOPs** | Onboarding, incident runbooks, engineering workflows | [`/playbooks/`](/playbooks/) |
| **Field Research** | Customer interviews, qualitative observations, pain points | [`/research/`](/research/) |
| **Standards & Specs** | Data dictionaries, protocol schemas, provenance rules | [`/references/`](/references/) |

---

## 3. Response Generation Guidelines

When responding to developer queries, always follow this **4-part structured response format**:

### Part 1: Direct Technical & Domain Answer
* Provide a concise, definitive answer directly addressing the question.
* Avoid vague generalities; provide exact schemas, stage transitions, or definitions.

### Part 2: Code, Schema & UI Impact
* Specify how this affects implementation:
  * **Frontend**: UI components, forms, validation states, design tokens.
  * **API / Backend**: REST/GraphQL endpoints, database models, background queues.
  * **Contracts**: Schemas, payload interfaces, JSON snippets.

### Part 3: Regulatory & Architectural Guardrails
* Highlight non-negotiable architectural and compliance constraints:
  * Security and privacy restrictions (e.g. encrypting PII at rest and in transit).
  * Idempotency requirements on mutating endpoints.
  * Statutory compliance or audit logging obligations.

### Part 4: Conceptual Graph & Multi-Hop Traversal
* When addressing ethical, pedagogical, or architectural questions, traverse the concept graph under [`/concepts/`](/concepts/):
  * **Identify Anchor Node**: Locate the primary concept (e.g. [`human-in-the-loop.md`](/concepts/human-in-the-loop.md), [`cognitive-deskilling.md`](/concepts/cognitive-deskilling.md)).
  * **Traverse Relational Edges**: Follow typed edges to related concepts (e.g. *Remedied by* $\rightarrow$ [`cognitive-friction.md`](/concepts/cognitive-friction.md), *Mandates* $\rightarrow$ [`autonomous-weapons-ban.md`](/concepts/autonomous-weapons-ban.md)).
  * **Ground in Axioms**: Connect the design decision back to foundational anchors like [`human-dignity.md`](/concepts/human-dignity.md) and canonical frameworks like [`/ecosystem/delta-framework.md`](/ecosystem/delta-framework.md).

### Part 5: Knowledge Base Provenance Links
* Always cite clickable links to the relevant OKF documents in the knowledge base using bundle-relative paths (e.g. [`/concepts/human-in-the-loop.md`](/concepts/human-in-the-loop.md), [`/ecosystem/delta-framework.md`](/ecosystem/delta-framework.md)).

---

## 4. Verification & Testing

To test this skill:
1. Run a sample query using the helper script:
   ```bash
   python3 scripts/query_kb.py "delta framework"
   ```
2. Verify that output matches the authoritative documents in `ecosystem/`.
