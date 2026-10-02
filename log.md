# Knowledge Base Changelog

## 2026-10-02
* **Bulk Institutional Retraction & Core Preservation**: Retracted and archived 17 external institution profiles into `archive/2026-10-02_041818_bulk_institutional_backout/`, establishing a streamlined normative core anchored by the **DeepMind Institute**, **The Rome Call & Hiroshima Appeal**, **The DELTA Framework**, and **Encyclical Letter Magnifica Humanitas**.
  - **Archived & Pruned Concepts**: `concepts/six-domains-wellbeing.md` (epistemic grounding depleted with Harvard profile retraction).
  - **Re-Grounded Concepts**: `concepts/eudaimonia.md` legitimately anchored in the DELTA Framework and DeepMind Institute's *Global Benefit from AI*.
  - **Surviving Grounding**: 26 concept nodes maintained authentic source provenance from the 4 core pillars.


## 2026-10-01
* **Source Retraction & Epistemic Decoupler**: Added [`scripts/backout_source.py`](/scripts/backout_source.py) and `/backout-source` skill to safely retract, substitute, and decouple external sources, papers, URLs, and institutional containers with dry-run blast radius auditing.
* **Archive & Reincorporation System**: Added [`scripts/reincorporate_source.py`](/scripts/reincorporate_source.py) to preserve backed-out assets in `archive/` with structured manifests and restore files, source citations, and reciprocal graph edges.
* **Presubmit & Validation Updates**: Updated [`scripts/validate.py`](/scripts/validate.py) and [`scripts/update_index.py`](/scripts/update_index.py) to exempt `archive/` packages from active validation and root index generation.
* **Ingestion**: Ingested [The DELTA Framework: Faith-Informed Virtue Ethics for Artificial Intelligence](/ecosystem/delta-framework.md) from [What is DELTA?](https://delta.nd.edu/what-is-delta/) and [DELTA Resources](https://delta.nd.edu/resources/) covering Notre Dame's virtue-ethics framework (Dignity, Embodiment, Love, Transcendence, Agency) and pedagogical/pastoral toolkits.
* **Ingestion**: Ingested [Encyclical Letter Magnifica Humanitas](/ecosystem/magnifica-humanitas.md) from [The Holy See](https://www.vatican.va/content/leo-xiv/en/encyclicals/documents/20260515-magnifica-humanitas.html) covering Pope Leo XIV's magisterial teaching on artificial intelligence, technocratic dominance, the dignity of labor, and the ban on autonomous weapons.
* **Institutions Area**: Established the Global AI Institutions & Research Labs Observatory in [/ecosystem/institutions/overview.md](/ecosystem/institutions/overview.md) to systematically track external AI research institutes, university ethics centers, standards bodies, and moral authorities.
* **Ingestion**: Ingested [The DeepMind Institute: Foundational Research, AGI Governance & Inaugural Essays](/ecosystem/institutions/deepmind-institute.md) from [DeepMind Institute](https://institute.deepmind.com/#essays) synthesizing the Institute's founding charter, governance model, and all eight inaugural essays on agent swarms, symbiotic intelligence, reasoning transparency, global benefit, and AGI economic policy.
* **Skill Upgrades**: Enhanced [`/ingest`](/skills/ingest/SKILL.md), [`/manage-knowledge-base`](/skills/manage-knowledge-base/SKILL.md), [`/ask-kb`](/skills/ask-kb/SKILL.md), and [`AGENTS.md`](/AGENTS.md) with dedicated support for ingesting institutional portals, publication series, multi-essay dossiers, and automatic registration in the Institutions Observatory.
* **Institution Template**: Added [`templates/institution-template.md`](/templates/institution-template.md) and [`skills/manage-knowledge-base/templates/institution_template.md`](/skills/manage-knowledge-base/templates/institution_template.md) providing a standardized structure for profiling external AI institutes, frontier labs, and moral authorities.
* **Institutional Expansion**: Ingested comprehensive dossiers into the Global AI Institutions Observatory covering:
  * **Harvard Human Flourishing Program**: Empirical research on character, eudaimonia, well-being domains, and critique of synthetic intimacy.
  * **UN High-Level Advisory Body on AI**: September 2024 final report *Governing AI for Humanity*, establishing 7 structural pillars to bridge the global governance deficit.
  * **Council of Europe AI Framework Convention**: The world's first legally binding international treaty on AI (CETS No. 225) protecting human rights, democracy, and rule of law.
  * [Rome Call for AI Ethics & Hiroshima Appeal](/ecosystem/institutions/rome-call-hiroshima.md): July 2024 historic expansion of algor-ethics to Eastern religions and categorical moral ban on lethal autonomous weapons.
  * **Oxford Institute for Ethics in AI**: Aristotelian virtue ethics, HAI Lab, and the landmark *Positive Alignment* research agenda for human flourishing.
  * **MIT AI & Education Working Group**: August 2026 landmark report on cognitive surrender, assessment collapse, and preserving productive struggle.
  * **Stanford Institute for Human-Centered AI (HAI)**: Human augmentation charter, foundation model transparency (HELM, AI Index), and educational cognitive agency.
  * **Anthropic Safeguards & Alignment**: Public Benefit Corporation charter, Constitutional AI, mechanistic interpretability (scaling monosemanticity), and Responsible Scaling Policy (RSP).
  * **UNESCO AI Ethics Sector**: 193-nation Recommendation on the Ethics of AI, Readiness Assessment Methodology (RAM), and Global South capacity building.
  * **Leverhulme Centre for the Future of Intelligence**: Cambridge research on pragmatic utopianism (Stephen Cave), AI narratives, and long-term civilizational futures.
  * **Center for Human-Compatible AI (CHAI)**: UC Berkeley research on provably beneficial AI (Stuart Russell), Assistance Games, the Off-Switch Game, and autonomous weapon bans.
  * **European AI Office**: European Commission statutory regulator enforcing the EU AI Act (Regulation 2024/1689), GPAI codes of practice, and prohibited practices.
  * **OECD.AI Policy Observatory**: Directorate for Science, Technology & Innovation; revised 2024 AI Principles on inclusive growth, well-being, and trustworthy AI.
  * **Institute for Human Flourishing (IHF)**: Rockefeller and Schmidt backed research-action lab on labor-using AI, frontline worker agency, and agrarian data sovereignty.
  * **Harvard University Overview**: Overarching profile uniting empirical flourishing research and Socratic pedagogical engineering.
  * **Harvard AI Pedagogy & Socratic Learning**: Derek Bok Center frameworks, CS50 Socratic assistant (*cs50.ai*), and negative constraints against direct answer generation.
  * **Carnegie Mellon University Simon Initiative**: Learning engineering, cognitive load modeling, GAITAR empirical classroom studies, and faded scaffolding.
  * **The Russell Group**: Joint 5-principle accord across 24 leading UK research universities on AI literacy, assessment adaptation, and academic integrity.
  * **Stanford University & HAI**: Enriched with Stanford Accelerator for Learning & ETS 2026 white paper *Responsible Assessment in the AI Era* (process data over product grading).
  * **UNESCO AI Ethics Sector**: Enriched with *Guidance for Generative AI in Education and Research* (age boundaries, teacher sovereignty).
* **Template Cleanup**: Removed obsolete starter template files (`concepts/future-initiative.md`, `systems/core-architecture.md`, `ecosystem/industry-landscape.md`), personalized `knowledge.config.json` for St. Francis High School's AI Initiative, and retained `research/user-interview-example.md` as an exemplar for Human-Centered Design (HCD) research.

## 2026-09-26
* **Agent Guidelines**: Added [`AGENTS.md`](/AGENTS.md) repository-wide operating contract for autonomous AI agents.
* **Knowledge Advisor Skill**: Added [`/ask-kb`](/skills/ask-kb/SKILL.md) and [`scripts/query_kb.py`](/scripts/query_kb.py) CLI & programmatic search tool.
* **Knowledge-Driven Engineering**: Added [`playbooks/knowledge-driven-engineering.md`](/playbooks/knowledge-driven-engineering.md) defining spec-driven development, AI pair programming, compliance PR reviews, and concept graduation.
* **Repository Initialized**: Extracted self-contained, self-maintaining knowledge base template conforming to Google OKF v0.2.
* **Architecture Groundwork**: Established core taxonomies across `/systems/`, `/ecosystem/`, `/concepts/`, `/playbooks/`, `/research/`, and `/references/`.
* **Tooling Configured**: Automated presubmit gatekeeper, bundle validator, and dynamic index generator verified.