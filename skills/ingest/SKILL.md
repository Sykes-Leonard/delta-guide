---
name: ingest
type: Skill
title: "Ingest URL Content into Knowledge Base"
description: "Downloads external web content from a URL, analyzes its relevance to the organization, asks the user for placement confirmation, and synthesizes it into an OKF v0.2 knowledge document."
status: stable
generated:
  by: agent:antigravity
  at: 2026-09-26T00:00:00Z
verified:
  - by: human:architecture-lead
    at: 2026-09-26T00:00:00Z
---

# Ingest URL Content into the Knowledge Base

This skill enables any agent to download content from an external URL, thoughtfully analyze its relevance to the organization's systems and strategy, interactively ask the user where in the knowledge base it should be placed, and synthesize it into a clean, well-structured **Google Open Knowledge Format (OKF v0.2)** document.

---

## 1. Trigger Phrases & Invocation

Activate this skill whenever the user says:
- `ingest <url>`
- `ingest https://...`
- `ingest this article: <url>`
- `add <url> to the knowledge base / wiki`
- `import documentation from <url>`

---

## 2. The 5-Step Ingest Workflow

```mermaid
flowchart TD
    A["1. User provides URL<br>('ingest <url>')"] --> B["2. Fetch Content<br>(read_url_content or fetch_content.py)"]
    B --> C["3. Analyze & Classify<br>(Identify Core Domain & Org Impact)"]
    C --> D{"4. Interactive Consultation<br>(ask_question: Confirm Destination)"}
    D -->|User Selects Path| E["5. Synthesize & Author OKF Document<br>(Frontmatter, Summary, Implications, Cross-links)"]
    E --> F["6. Sync & Audit<br>(update_index.py & validate.py)"]
```

---

### Step 1: Fetch and Extract the URL Content
1. Use `read_url_content` with the provided URL to retrieve clean markdown text.
2. If `read_url_content` is unavailable or returns an error, run the helper script:
   ```bash
   python3 skills/ingest/scripts/fetch_content.py "<URL>"
   ```
3. Extract metadata:
   - **Document Title**: Official title from `<title>` or primary `h1`.
   - **Source Organization / Publisher**: Authoritative agency, corporation, or standards body.
   - **Publication Date**: If available.
   - **Core Themes**: Regulation, API changes, competitor benchmarks, user research, architecture standards.

---

### Step 2: Thoughtful Semantic Classification
Evaluate the content against the knowledge base taxonomy:

| Destination Category | Scope & Criteria | Typical Document Types |
| :--- | :--- | :--- |
| **`ecosystem/institutions/`** | **"What Is" (External Institutions)**: Key external research institutes, frontier labs, university centers, and standards bodies. | Institutional profiles, governance charters, multi-paper dossiers, lab roadmaps. |
| **`ecosystem/`** | **"What Is" (External Reality)**: External laws, statutory regulations, partner platforms, payment rails, industry standards. | Government policies, partner API releases, compliance regulations. |
| **`systems/`** | **"What Is" (Internal Reality)**: Active production architecture, codebases, data models, or service documentation. | Service specs, API endpoints, schema definitions, internal workflows. |
| **`concepts/`** | **Foundational Concepts & Proposals**: Theoretical constructs, architectural RFCs, foundational models, concept clusters. | Product RFCs, new feature proposals, concept clusters, feasibility studies. |
| **`frontier/`** | **"What Could Be" (Frontier Explorations)**: Nascent initiatives, exploratory prototypes, and horizon scanning. | Horizon scan notes, prototype specs, emerging technology evaluations. |
| **`playbooks/`** | **Operational SOPs**: Step-by-step human or agent runbooks. | Setup checklists, incident playbooks, deployment runbooks. |
| **`research/`** | **Field Research**: Qualitative research, user interviews, surveys. | Transcripts, user observation notes, customer feedback. |
| **`references/`** | **Specifications & Standards**: Foundational reference specifications. | Data dictionaries, protocol standards, format guidelines. |

---

### Step 3: Mandatory User Confirmation via `ask_question`
**DO NOT write the file before asking the user!**
Formulate an interactive multiple-choice question using `ask_question`:

* **Question**: `"Where in the knowledge base would you like to place this content?"`
* **Options**:
  - Always list your **recommended placement first** prefixed with `(Recommended)` and a brief rationale.
  - Provide 2–3 plausible alternative categories.
  - Format options as clear paths with short explanations.

*Example `ask_question` Call*:
```json
{
  "questions": [
    {
      "question": "I analyzed the external specification. Where should this be placed in the knowledge base?",
      "is_multi_select": false,
      "options": [
        "(Recommended) ecosystem/new-payment-api-standard.md (External partner API standard under 'What Is')",
        "concepts/payment-gateway-upgrade.md (Product RFC proposal for upgrading internal payments)",
        "playbooks/payment-integration-runbook.md (Operational runbook for integrating the API)"
      ]
    }
  ],
  "toolSummary": "Confirming knowledge base destination",
  "toolAction": "Asking user for content placement"
}
```

---

### Step 3b: Special Workflow — Ingesting Institutional Portals & Publication Hubs
When ingesting an institution's public portal or research hub (e.g. university research centers, industry labs, or standards bodies):

1. **Child Publication Discovery**:
   * Inspect the hub page for linked articles, white papers, or technical essays.
   * Extract key metadata (titles, authors, dates, abstracts, and canonical URLs) across the entire series.
2. **Interactive Structural Choice**:
   * Use `ask_question` to offer the user a clear structural choice:
     * **Unified Institutional Dossier** (`ecosystem/institutions/<slug>.md`): A comprehensive document capturing the institutional profile, leadership, mission, and synthesizing the publication series with dedicated subsections.
     * **Subfolder Structure** (`ecosystem/institutions/<slug>/`): Dedicated subfolder containing an overview file plus individual standalone markdown files for each publication.
3. **Comparative Alignment Analysis**:
   * Include a comparative synthesis section relating the institution's stances to existing organizational principles and systems architecture.

---

### Step 4: Synthesize the OKF v0.2 Document
Never do a raw copy-paste dump of the webpage text. Thoughtfully synthesize the content into an executive-grade OKF document:

1. **Strict YAML Frontmatter**:
   ```yaml
   ---
   type: <Ecosystem Context | Technical Specification | Concept | Playbook | Research Notes>
   title: "Accurate Descriptive Title"
   description: "Single-sentence executive summary of the content and its importance."
   tags: [tag1, tag2, tag3]
   status: stable  # Use 'draft' if exploratory concept
   generated:
     by: agent:ingest
     at: <ISO 8601 UTC timestamp>
   verified: []
   sources:
     - id: source:<slug>
       resource: <ORIGINAL_URL>
       title: "<Publication Name / Article Title>"
   ---
   ```

2. **Standard Document Sections**:
   - `# [Title]`
   - `## 1. Executive Summary`: Concise 2–3 paragraph synthesis of the source.
   - `## 2. Core Policies, Directives & Data`: Key findings, statutory articles, technical parameters, or operational tables extracted from the source.
   - `## 3. Strategic Implications for the Organization`: Explicit breakdown of how this affects our systems, team operations, or product roadmap.
   - `## 4. Key Reference Points & Excerpts`: High-signal quotes or data tables from the original text.
   - `## 5. Related Knowledge Base Documents`: Bundle-relative links to related documents in the knowledge base.

---

### Step 5: Concept Graph Extraction & Mind Map Linkage
After synthesizing the primary ecosystem or institution document:
1. **Extract Core Concepts**:
   * Identify 1–3 novel conceptual claims, architectural patterns, or governance tensions introduced by the source.
2. **Cross-Link Existing Concepts**:
   * Inspect [`/concepts/`](/concepts/) to see if related concepts already exist.
   * Add citations and cross-links from those existing concept documents back to the newly ingested source.
3. **Author New Concept Nodes**:
   * If the ingested material introduces a novel concept not yet captured, author a new concept document under `/concepts/` using [`templates/concept-template.md`](/templates/concept-template.md).
   * Assign the new concept to its appropriate thematic cluster in [`/concepts/`](/concepts/) and update the cluster's Constituent Concepts Matrix.
   * Add inbound and outbound edges in the concept's `Relational Edge Index` table and Mermaid diagram.

---

### Step 6: Synchronize Index, Log, and Validate
Once the document and concept linkages are saved:
1. **Regenerate Index**:
   ```bash
   python3 scripts/update_index.py
   ```
2. **Append to `log.md`**:
   Add an entry under the current date:
   ```markdown
   * **Ingestion**: Ingested [<Title>](/<relative-path>) from [<Source Title>](<URL>) covering [topic].
   ```
3. **Run Presubmit Gatekeeper**:
   ```bash
   python3 scripts/presubmit.py
   ```
