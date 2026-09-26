---
type: Reference
title: "Google OKF v0.2 Quick Reference Cheat Sheet"
description: "Reference cheat sheet for Open Knowledge Format frontmatter fields and conventions."
status: stable
---

# Google OKF v0.2 Quick Reference Cheat Sheet

## Frontmatter Fields

| Field | Necessity | Format / Allowed Values | Purpose |
| :--- | :---: | :--- | :--- |
| `type` | **REQUIRED** | String (e.g. `Concept`, `Playbook`) | Categorization & routing. |
| `title` | Recommended | String | Display name. |
| `description` | Recommended | String | Single-sentence summary for indexes. |
| `resource` | Optional | URI / Path | Canonical link to underlying system/repo. |
| `tags` | Optional | YAML List | Search and filtering keywords. |
| `status` | Optional | `draft` \| `stable` \| `deprecated` | Lifecycle stage (default: `stable`). |
| `stale_after` | Optional | ISO 8601 Datetime | Expiration timestamp. |
| `generated` | Optional | `{ by: <actor>, at: <iso_dt> }` | Creation metadata. |
| `verified` | Optional | List of `{ by: <actor>, at: <iso_dt> }` | Trust & verification history. |
| `sources` | Optional | List of `{ id, resource, title }` | Provenance sources. |

---

## Actor Conventions

- `human:<username>` - Human authors/reviewers (e.g., `human:jane`).
- `<agent_name>/<model>` - AI agents (e.g., `agent:antigravity`).
- `process:<pipeline_name>` - Automated processes (e.g., `process:nightly-sync`).

---

## Trust Tier Derivation

- **Unverified**: No `verified` field.
- **Machine-Confirmed**: Verified solely by non-`human:` actors.
- **Human-Reviewed**: At least one `human:<id>` verification event present.

---

## Cross-Linking

- Bundle-relative: `/concepts/future-initiative.md` (anchored to bundle root).
- Relative: `./other.md` or `../playbooks/onboarding-guide.md`.
