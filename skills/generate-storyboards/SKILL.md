---
name: generate-storyboards
type: Skill
title: "Generate Storyboards for Product Concepts"
description: "Generate high-impact sequential visual storyboards and accompanying product specifications for product concepts, user journeys, and ecosystem integrations."
status: stable
generated:
  by: agent:antigravity
  at: 2026-09-26T00:00:00Z
verified:
  - by: human:product-team
    at: 2026-09-26T00:00:00Z
---

# Generate Storyboards for Product Concepts

This skill equips agents to conceptualize, illustrate, and document end-to-end product features and user journeys as structured visual storyboards.

---

## 1. When to Use This Skill

Activate this skill whenever:
- Designing a new product workflow, customer-facing feature, or partner integration (e.g. payment rails, messaging/triage, third-party APIs).
- Visualizing a user journey across multiple actors (e.g. end user/customer, front desk/support, operations staff, specialist/manager, external system/regulatory body).
- Communicating a new product concept to executive stakeholders, design advisors, or engineering leads through visual graphics and narrative scripts.
- Documenting approved product concepts in the Open Knowledge Base (`concepts/` or `storyboards/`).

---

## 2. Core Storyboarding & Design Principles

Every storyboard should reflect the authentic operational realities of the target domain:

1. **Authentic Operational Reality**:
   - Ground the storyboard in the authentic physical and digital environment of your users (office, mobile, field, retail, clinical, or logistics).
   - Technology mix: Low-bandwidth mobile web / PWA on customer smartphones, paired with modern desktop browsers or tablets running operational workstations.

2. **Visual Design Identity**:
   - Primary Slate Navy: `#475f7b` (or organization primary brand color)
   - Secondary Accent: `#5ba065` (or organization accent)
   - Light Clean Backgrounds: `#f8f9fa`
   - Warm, welcoming, respectful, and dignified human interactions with clear typography and crisp vector illustration.

3. **Operational & System Boundaries**:
   - Differentiate lightweight automated or client-side intake from full operational or specialist review.
   - Clarify where automation **initiates, validates, and pre-stages data to get the process moving**, while human operators or downstream services complete authoritative processing and resolution.

---

## 3. Standard Storyboard Grid Layouts

### Option A: The 6-Panel Balanced Grid (Recommended for Complex Features)
* **Aspect Ratio**: `16:9`
* **Grid**: 2 rows of 3 panels (3 on top row, 3 on bottom row)
* **Narrative Arc**:
  - **Panel 1 (Platform Setup)**: System onboarding, administrative setup, or rule configuration.
  - **Panel 2 (Discovery)**: User discovers service remotely or trigger event occurs (search, map, messaging, notification, or referral).
  - **Panel 3 (Lightweight Action)**: Minimal mobile/web data capture (< 4 fields) optimized for quick user interaction.
  - **Panel 4 (System Staging / Background Pre-Fill)**: Pre-fills intake records, stages queues, or performs automated checks to get the ball rolling before arrival.
  - **Panel 5 (Frictionless Arrival / Interaction)**: Seamless interaction on-site or in-app with zero redundant paperwork or duplicate entries.
  - **Panel 6 (Operational Sync & Resolution)**: Instant backend synchronization, specialist sign-off, and clean closure.

### Option B: The 4-Panel Linear Strip (Best for Simple User Journeys)
* **Aspect Ratio**: `16:9`
* **Grid**: 4 horizontal panels (or 2x2 grid)
* **Narrative Arc**: Discovery $\rightarrow$ Lightweight Action $\rightarrow$ System Processing $\rightarrow$ Operational Resolution.

---

## 4. Step-by-Step Execution Workflow

### Step 1: Draft the Narrative Arc & Touchpoint Table
Define:
- **Actors**: User persona, frontline staff/operator, specialist/manager.
- **Pain Point**: Why the existing paper or manual workflow fails (long lines, manual tallies, missing records, drop-offs).
- **Intervention**: How the digital capability eliminates friction and automates touchpoints.

### Step 2: Generate the Visual Graphic via `generate_image`
Construct an image generation prompt using the proven pattern:
```text
A professional, clean [4-panel | 6-panel] sequential storyboard graphic infographic arranged in a clean [horizontal strip | 2x3 grid] illustrating [concept title].

Style: Clean modern vector editorial illustration with crisp outlines, warm colors, authentic professional setting, clearly numbered panels from 1 to [N].

Panel 1 - '1. [Action]': [Scene description, actors, UI inset, callout text]
Panel 2 - '2. [Action]': ...
...
Panel N - 'N. [Action]': ...

Labels: 1. [...], 2. [...], ..., N. [...]
```

### Step 3: Archive the Concept in `concepts/`
Create a dedicated concept file in `concepts/<feature-slug>.md` (or `storyboards/<feature-slug>.md`) adhering to **Google OKF v0.2**:
- YAML Frontmatter with `type: Product Storyboard`
- Embedded visual graphic from `assets/` (or `concepts/assets/`)
- Full narrative walkthrough with scene settings, dialogue, and UI states
- Mermaid Sequence Diagram detailing technical touchpoints
- Expected operational and business metrics

### Step 4: Export Deliverables for Stakeholders
When stakeholders need executive review artifacts:
1. Export a formatted `.docx` file with the embedded graphic and tables using `python3 skills/generate-storyboards/scripts/export_storyboard_docx.py`.
2. Provide a clipboard-friendly `.html` file for 1-click copy into [docs.new](https://docs.new).

### Step 5: Update Bundle Index & Validate
1. Run `python3 scripts/presubmit.py` (or `python3 scripts/update_index.py`)
2. Append change summary to `log.md`
3. Confirm bundle validation passes with 0 errors (`python3 scripts/validate.py`).
