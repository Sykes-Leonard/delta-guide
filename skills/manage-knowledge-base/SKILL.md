---
name: manage-knowledge-base
type: Skill
title: "Manage Knowledge Base (OKF v0.2)"
description: "Navigate, read, author, update, and validate the markdown knowledge base according to Google OKF v0.2."
status: stable
generated:
  by: agent:antigravity
  at: 2026-09-26T00:00:00Z
verified:
  - by: human:architecture-lead
    at: 2026-09-26T00:00:00Z
---

# Manage Knowledge Base (Google OKF v0.2)

This skill equips any AI agent to manage, traverse, extend, and audit this knowledge repository. The repository strictly adheres to the **Google Open Knowledge Format (OKF v0.2)** standard.

---

## 1. When to Use This Skill

Activate this skill whenever you need to:
* **Discover & Research**: Find authoritative context on active production systems, architecture, external regulatory realities, or proposed product features.
* **Author New Concepts**: Create new markdown documentation for features, APIs, system components, or operational runbooks.
* **Maintain & Update**: Update existing concept files, increment trust events (`verified`), manage document lifecycles (`status`, `stale_after`), or record changes in `log.md`.
* **Audit & Validate**: Ensure frontmatter schema conformance and verify that zero broken links exist within the bundle.

---

## 2. Directory Architecture & Taxonomy

The knowledge bundle organizes information with a clean architectural demarcation between current reality ("What Is") and future proposals ("What Could Be"):

```text
.
├── index.md                 # Root directory listing (declares okf_version: "0.2")
├── log.md                   # Chronological update history (ISO 8601 date headings)
├── knowledge.config.json    # Org metadata and categorized section configuration
│
├── ecosystem/               # "WHAT IS" - External Reality & Regulatory Infrastructure
│   ├── institutions/        # External research institutes, frontier labs & moral authorities
│   └── ...                  # Partner APIs, external laws, industry standards
│
├── systems/                 # "WHAT IS" - Current Production Systems & Workflows
│   └── ...                  # Production services, databases, data models, APIs
│
├── concepts/                # Theoretical Concepts, Ethical Frameworks & Clusters
│   └── ...                  # Foundational models, virtue-ethics constructs, thematic clusters
│
├── frontier/                # "WHAT COULD BE" - Emerging Ideas, Prototypes & Horizon Scanning
│   └── ...                  # Nascent initiatives, exploratory prototypes, and emerging proposals
│
├── playbooks/               # Operational guides, developer setups, and runbooks
├── research/                # Raw field research notes, customer interviews & qualitative findings
├── references/              # Standards, specifications, data schemas & provenance
├── templates/               # Reusable starter templates for new documents
└── scripts/                 # Self-contained bundle maintenance & presubmit scripts
```

---

## 3. Agent Operating Procedures

### Procedure A: Traversing & Reading (Progressive Disclosure)
1. **Always start at [`index.md`](file:///index.md)**.
   * Do NOT read all files in the repository.
   * Read `index.md` first to inspect the one-line summaries of each document.
2. **Follow bundle-relative links**:
   * Links starting with `/` (e.g., `[DELTA Framework](/ecosystem/delta-framework.md)`) are bundle-relative, anchored to the repository root.
3. **Distinguish "What Is" vs "What Could Be"**:
   * `/ecosystem/` and `/systems/`: Represents current reality (`status: stable`).
   * `/concepts/`: Represents foundational theoretical models and concept clusters.
   * `/frontier/`: Represents future exploratory proposals and emerging prototypes (`status: draft`).
4. **Evaluate Trust & Freshness**:
   * Check `stale_after`: If `now >= stale_after`, treat information as potentially outdated.
   * Check `verified`: Entries containing `human:<id>` represent human-certified ground truth.

---

### Procedure B: Authoring a New Concept vs. System Fact
1. **Choose the appropriate subdirectory**:
   * **Is it "What Is"?**
     * External research institutes, frontier AI labs, or moral authorities $\rightarrow$ `ecosystem/institutions/` (`status: stable`; register in [`/ecosystem/institutions/overview.md`](/ecosystem/institutions/overview.md))
     * External environment, statutory regulations, or partner platforms $\rightarrow$ `ecosystem/` (`status: stable`)
     * Existing production software, APIs, or database schemas $\rightarrow$ `systems/` (`status: stable`)
     * Operational runbook or incident response guide $\rightarrow$ `playbooks/` (`status: stable`)
     * Customer interview or observation transcript $\rightarrow$ `research/` (`status: stable`)
   * **Theoretical Concept or Framework?**
     * Foundational theoretical construct, ethical framework, or concept cluster $\rightarrow$ `concepts/` (`status: stable` or `draft`, must register in a thematic cluster)
   * **Emerging New Idea or Prototype?**
     * Emerging innovation, exploratory prototype, or horizon-scanning proposal $\rightarrow$ `frontier/` (`status: draft`, use [`templates/frontier-template.md`](/templates/frontier-template.md))
2. **Add Strict OKF v0.2 Frontmatter**:
   Every concept document MUST begin with YAML frontmatter:
   ```yaml
   ---
   type: <System Component | Ecosystem Context | Concept | Frontier Exploration | Playbook | Research Notes | Reference>
   title: "Display Title"
   description: "Single-sentence summary of the document."
   tags: [tag1, tag2]
   status: stable  # or 'draft'
   generated:
     by: <your_agent_name_or_id>
     at: <ISO 8601 UTC timestamp>
   verified:
     - by: <verifier_actor>
       at: <ISO 8601 UTC timestamp>
   sources:
     - id: <stable-id>
       resource: <path or url>
       title: <Human-readable source name>
   ---
   ```
3. **Format the Markdown Body**:
   * Use structured headings (`## 1. Overview`, `## 2. Architecture`, etc.).
   * Favor tables, bulleted lists, and Mermaid diagrams over dense prose.
   * Cite internal bundle links using bundle-relative paths (e.g. `/ecosystem/delta-framework.md`).

---

### Procedure C: Synchronizing Indexes & Update Logs
Whenever a concept is added, updated, or deprecated:
1. **Sync Root Index**:
   Run the self-contained index generator script:
   ```bash
   python3 scripts/update_index.py
   ```
2. **Append to `log.md`**:
   Add an entry under the current date (`## YYYY-MM-DD`):
   ```markdown
   ## 2026-09-26
   * **Creation**: Added [New Feature](/concepts/new-feature.md) describing the proposed capability.
   ```

---

### Procedure E: Managing Concept Clusters & Mind Map Edges
When authoring or modifying documents under `/concepts/`:
1. **Never Create Orphan Concepts**:
   * Every new concept must be assigned to one of the 5 canonical concept clusters (`cluster-human-flourishing.md`, `cluster-moral-agency.md`, `cluster-power-governance.md`, `cluster-embodiment-presence.md`, `cluster-transcendence-truth.md`) or define a new cluster using [`templates/concept-cluster-template.md`](/templates/concept-cluster-template.md).
   * Update the cluster's `## 3. Constituent Concepts Matrix` to register the new concept.
2. **Build and Maintain Relational Edges**:
   * Every concept document must include a `## 6. Relational Edge Index` with a Markdown table defining typed inbound/outbound relationships.
   * Use canonical relationship verbs (*Grounds*, *Requires*, *Opposes*, *Operationalized as*, *Threatened by*, *Remedied by*, *Cultivated via*, *Mandates*, *Enforces*, *Bridges*, *Critiques*).
   * When adding an edge from Concept A to Concept B, update *both* files' edge tables and Mermaid diagrams to maintain graph reciprocity.
3. **Mandatory External Source Provenance**:
   * In frontmatter, populate the `sources:` block with stable external identifiers (`id`, `resource` URL, `title`) citing foundational academic papers, official treaties, or papal encyclicals.
4. **Preserve Mermaid Mind Map Syntax**:
   * Keep the `## 2. Conceptual Mind Map & Relational Edges` Mermaid diagram synchronized with the edge index table.

---

### Procedure F: Bundle Validation & Auto-Fixing
Before concluding any task that touches documentation, run the bundle's self-contained presubmit hook or validator:

```bash
# 1. Run presubmit gatekeeper (auto-fixes frontmatter, links, compiles graph, and validates)
python3 scripts/presubmit.py

# 2. Rebuild interactive concept graph viewer
python3 scripts/build_viewer.py

# 3. Or run validator directly with auto-fix flag
python3 scripts/validate.py --fix
```

The presubmit hook:
* Automatically refreshes and synchronizes `index.md` from concept frontmatter using `knowledge.config.json`.
* Automatically generates missing OKF v0.2 YAML frontmatter blocks (`type`, `title`, `description`, `status`).
* Strips illegal frontmatter from subdirectory `index.md` (OKF §8) and `log.md` (OKF §9).
* Repairs broken links with missing `.md` extensions or malformed relative paths.
* Automatically stages repaired files if running within a Git commit pre-commit hook.

Ensure:
* 0 Errors (Frontmatter is valid YAML, required `type` is present, reserved filenames adhere to rules).
* 0 Warnings (Zero broken bundle-relative or relative links, no stale unflagged documents).

---

## 4. Self-Contained Maintenance Scripts

* **Presubmit Hook**: [`scripts/presubmit.py`](file:///scripts/presubmit.py) - Gatekeeper running auto-fix and bundle validation before commit.
* **Validator & Fixer**: [`scripts/validate.py`](file:///scripts/validate.py) - Validates bundle syntax, links, and trust tiers (`--fix` to auto-repair).
* **Index Generator**: [`scripts/update_index.py`](file:///scripts/update_index.py) - Synchronizes `index.md` from concept frontmatter.
* **Specification Reference**: [`references/okf_cheat_sheet.md`](file:///skills/manage-knowledge-base/references/okf_cheat_sheet.md) - Quick syntax reference for OKF fields.
