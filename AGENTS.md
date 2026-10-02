---
type: Reference Standard
title: "AI Agent Guidelines & Operating Contract"
description: "Repository-level operating rules and architectural constraints for AI agents interacting with this codebase and knowledge base."
tags: [agent-instructions, guidelines, okf]
status: stable
generated:
  by: agent:antigravity
  at: 2026-09-26T00:00:00Z
verified:
  - by: human:architecture-lead
    at: 2026-09-26T00:00:00Z
---

# AI Agent Guidelines & Operating Contract

Welcome to the engineering workspace. You are assisting in building, maintaining, and documenting digital software solutions.

---

## 1. Ground Truth & Knowledge Base Root

The single source of truth for all architectural, statutory, and operational requirements is the **Open Knowledge Format (OKF v0.2)** knowledge base in this repository.

* **Start Here**: Read [`index.md`](file:///index.md) for progressive disclosure of concepts, production systems, and ecosystem realities.
* **Domain & Architecture Questions**: Always consult the knowledge base or invoke the `/ask-kb` skill before making assumptions about system architecture or business constraints:
  * DELTA Framework & Virtue Ethics: [`/ecosystem/delta-framework.md`](/ecosystem/delta-framework.md)
  * Papal AI Doctrine & Human Dignity: [`/ecosystem/magnifica-humanitas.md`](/ecosystem/magnifica-humanitas.md)
  * Engineering lifecycle & SDD process: [`/playbooks/knowledge-driven-engineering.md`](/playbooks/knowledge-driven-engineering.md)

---

## 2. Non-Negotiable Compliance Rules

1. **Data Protection & Privacy**:
   * **Never** commit, log, or leak unmasked Personally Identifiable Information (PII), customer secrets, or credentials into client logs, telemetry, or unencrypted storage.
2. **Reality vs. Proposals Demarcation**:
   * Always differentiate active production systems (`/systems/`, `status: stable`) from future exploratory proposals (`/concepts/`, `status: draft`).
3. **Resilience & Graceful Degradation**:
   * Client applications and prototypes must degrade gracefully during intermittent network connectivity, using optimistic updates and local caching.
4. **Idempotency**:
   * Mutating operations must support idempotent request tokens to prevent duplicate side effects on retries.

---

## 3. Workspace Layout

* `index.md`: Root progressive disclosure index listing all categorized documents.
* `systems/`: "What Is" — Active production software, services, schemas, and workflows.
* `ecosystem/`: "What Is" — External regulatory environment, standards, partner rails.
* `concepts/`: "What Could Be" — Feature proposals, product RFCs, architectural explorations.
* `playbooks/`: Operational runbooks, developer setup guides, team SOPs.
* `research/`: Customer discovery interviews, user observations, qualitative feedback.
* `references/`: Format standards, schemas, data dictionaries, provenance guidelines.
* `scripts/`: Self-contained Python stdlib maintenance and validation tools.
* `skills/`: Reusable autonomous AI agent capabilities.
* `templates/`: Standardized authoring templates.

---

## 4. Agent Skills & Slash Commands

When interacting with the user or executing complex tasks, use these registered skills:
* `/ask-kb <query>`: Instant architectural, statutory, and domain consulting.
* `/manage-knowledge-base`: Validate, author, or update the OKF bundle.
* `/ingest <url>`: Ingest external web content, specifications, or policies into OKF format.

---

## 5. Maintenance & Presubmit Gatekeeper

Before completing tasks that modify markdown documentation:
1. Run `./scripts/presubmit.py` to auto-fix frontmatter, repair links, and synchronize `index.md`.
2. Ensure validation passes with 0 errors and 0 warnings.
