---
type: Reference
title: "Google Open Knowledge Format Specification"
description: "Canonical summary of the Google OKF v0.2 specification, trust tiers, and conventions."
resource: https://github.com/GoogleCloudPlatform/open-knowledge-format
tags: [okf, standards, google-cloud, specification, agent-wiki]
status: stable
generated:
  by: agent:antigravity
  at: 2026-09-26T00:00:00Z
verified:
  - by: human:architecture-lead
    at: 2026-09-26T00:00:00Z
sources:
  - id: okf-spec-v02
    resource: https://raw.githubusercontent.com/GoogleCloudPlatform/open-knowledge-format/main/SPEC.md
    title: "Open Knowledge Format (OKF) Version 0.2 Specification"
---

# Google Open Knowledge Format (OKF) Specification v0.2

## 1. Overview
The **Open Knowledge Format (OKF)** is a vendor-neutral specification published by Google Cloud for representing institutional knowledge as a directory of plain Markdown files with YAML frontmatter.

It standardizes the "LLM Wiki" pattern:
* **Zero Proprietary Databases**: If you can `cat` a file, you can read it; if you can `git clone` a repo, you can distribute it.
* **Agent- & Human-Readable**: Clean structural markdown allows immediate comprehension by developers and LLM agents alike.
* **First-Class Provenance, Trust, and Lifecycle**: Explicit frontmatter metadata fields answer:
  1. *What was this created from?* (`sources`)
  2. *How much should I trust it?* (`verified`, trust tiers)
  3. *Is it still true?* (`stale_after`, `status`)
  4. *Who or what wrote it?* (`generated.by`, actor conventions)

---

## 2. Reserved Filenames

| Filename | Purpose | Allowed Frontmatter |
| :--- | :--- | :--- |
| `index.md` | Progressive disclosure directory listing | At bundle root only: `okf_version: "0.2"` |
| `log.md` | Chronological update log (`## YYYY-MM-DD`) | No frontmatter permitted |

---

## 3. Frontmatter Specification

```yaml
---
type: <Type name>             # REQUIRED: Short string (e.g. Concept, Playbook, System Component)
title: <Display Name>         # Recommended: Display title
description: <One-liner>      # Recommended: Single sentence summary for indexes
resource: <Canonical URI>     # Optional: Underlying URL or path
tags: [<tag1>, <tag2>]        # Optional: Cross-cutting categories
status: stable                # Optional: draft | stable | deprecated (default: stable)
stale_after: <ISO 8601>       # Optional: Content is considered stale on/after this datetime
generated:                    # Optional: Production metadata
  by: <actor>                 # REQUIRED within generated: e.g. agent:antigravity
  at: <ISO 8601 datetime>     # ISO 8601 UTC timestamp
verified:                     # Optional: Trust events
  - by: <actor>               # e.g. human:username or process:ci
    at: <ISO 8601 datetime>
sources:                      # Optional: Provenance list
  - id: <stable-id>
    resource: <URI or path>
    title: <Title>
---
```

---

## 4. Actor Conventions & Trust Tiers
* `human:<id>`: Human authors or reviewers (e.g., `human:jane`).
* `agent:<name>`: AI agents or tools (e.g., `agent:antigravity`).
* `process:<id>`: Automated processes or CI pipelines (e.g., `process:nightly-sync`).

### Trust Tiers
1. **Unverified**: No `verified` block.
2. **Machine-Confirmed**: Verified by non-`human:` actors only.
3. **Human-Reviewed**: Verified by at least one `human:<id>` actor.

---

## 5. Cross-Linking Conventions
* **Bundle-Relative (Recommended)**: Begins with `/` and resolves relative to the bundle root (e.g., `/concepts/future-initiative.md`).
* **Relative**: Standard relative link (e.g., `../systems/core-architecture.md`).
