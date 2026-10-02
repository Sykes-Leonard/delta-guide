---
type: Playbook
title: "Product Concept Storyboarding Playbook"
description: "Standard operating procedure for authoring visual storyboards and product concept specifications for features, user journeys, and partner integrations."
tags: [playbook, storyboard, product-design, visual-specification]
status: stable
generated:
  by: agent:antigravity
  at: 2026-09-26T00:00:00Z
verified:
  - by: human:product-team
    at: 2026-09-26T00:00:00Z
sources:
  - id: source:generate-storyboards-skill
    resource: /skills/generate-storyboards/SKILL.md
    title: "Generate Storyboards Skill"
---

# Product Concept Storyboarding Playbook

This playbook establishes the standard operating procedure for creating, visualising, and archiving product concept storyboards.

---

## 1. Objectives & Scope

Storyboards bridge abstract technical specifications with human-centered visual narratives. They are used to:
1. Align product, design, and engineering teams on end-to-end user journeys before code is written.
2. Communicate the value proposition to customers, executives, and external partners.
3. Validate operational handoffs, client/server boundaries, and third-party integrations.
4. Store permanent visual design references in the Knowledge Base (`concepts/` or `storyboards/`).

---

## 2. Standard 6-Panel Layout Pattern

For multi-actor or ecosystem workflows, follow the **balanced 2×3 grid (16:9 aspect ratio)**:

* **Top Row (Discovery & User Engagement)**:
  * **Panel 1 (Platform Setup)**: Initial user onboarding, tenant setup, or organizational configuration.
  * **Panel 2 (Discovery)**: User discovers the service or entry trigger occurs (search, map, notification, messaging, or referral).
  * **Panel 3 (Lightweight Action)**: Minimal digital data entry (< 4 fields) optimized for mobile smartphones or fast web interaction.
* **Bottom Row (System Staging & Operational Resolution)**:
  * **Panel 4 (Automated Pre-Fill & Staging)**: The captured data initiates and pre-fills records or stages queues to get the workflow moving prior to the live interaction.
  * **Panel 5 (Frictionless Arrival / Interaction)**: In-person arrival or synchronous session with zero redundant paperwork or duplicate questions.
  * **Panel 6 (System Sync & Resolution)**: Instant synchronization with backend databases and dashboards, allowing the operator/specialist to complete the task and sign off.

---

## 3. Authoring Guidelines

### Rule 1: Grounded in Operational Reality
* Portray authentic environments (field operations, mobile devices, customer kiosks, office workstations).
* Feature realistic identifiers, payment rails, and communication channels.

### Rule 2: Explicit System Boundaries
* Differentiate lightweight automated or client-side intake from authoritative back-office processing. Automated intake pre-stages records; human specialists or backend workers perform authoritative processing, review, and resolution.

### Rule 3: Visual Style Uniformity
* **Style**: Clean vector editorial digital illustration, warm lighting, crisp outlines, authentic professional settings.
* **Branding**: Slate Navy (`#475f7b`), Forest Accent (`#5ba065`), and light clean surfaces (`#f8f9fa`).
* **Labels**: Numbered step titles across each panel (e.g., `1. Platform Setup`, `2. Discovery`, etc.).

---

## 4. Archival & Deliverable Workflow

1. **Save Visual Assets**:
   Store master graphics in `concepts/assets/<concept_slug>.jpg` (or `storyboards/assets/<concept_slug>.jpg`).
2. **Author Storyboard Document**:
   Create `concepts/<concept_slug>.md` using the [OKF Storyboard Template](/templates/storyboard-template.md).
3. **Generate Stakeholder Deliverables**:
   Generate an executive `.docx` and clipboard-ready HTML for distribution via Google Docs:
   ```bash
   python3 skills/generate-storyboards/scripts/export_storyboard_docx.py <image_path> "<Title>" [output_prefix]
   ```
4. **Update Indexes & Validate**:
   Run the bundle gatekeeper:
   ```bash
   ./scripts/presubmit.py
   ```

---

## 5. Related Knowledge Base Documents

* [Generate Storyboards Skill](/skills/generate-storyboards/SKILL.md)
* [OKF Storyboard Template](/templates/storyboard-template.md)
* [Knowledge-Driven Engineering](/playbooks/knowledge-driven-engineering.md)
* [Core Architecture Overview](/systems/core-architecture.md)
