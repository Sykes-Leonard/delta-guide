# Knowledge Base Changelog

## 2026-10-01
* **Ingestion**: Ingested [The DELTA Framework: Faith-Informed Virtue Ethics for Artificial Intelligence](/ecosystem/delta-framework.md) from [What is DELTA?](https://delta.nd.edu/what-is-delta/) and [DELTA Resources](https://delta.nd.edu/resources/) covering Notre Dame's virtue-ethics framework (Dignity, Embodiment, Love, Transcendence, Agency) and pedagogical/pastoral toolkits.
* **Ingestion**: Ingested [Encyclical Letter Magnifica Humanitas](/ecosystem/magnifica-humanitas.md) from [The Holy See](https://www.vatican.va/content/leo-xiv/en/encyclicals/documents/20260515-magnifica-humanitas.html) covering Pope Leo XIV's magisterial teaching on artificial intelligence, technocratic dominance, the dignity of labor, and the ban on autonomous weapons.
* **Institutions Area**: Established the Global AI Institutions & Research Labs Observatory in [/ecosystem/institutions/overview.md](/ecosystem/institutions/overview.md) to systematically track external AI research institutes, university ethics centers, standards bodies, and moral authorities.
* **Ingestion**: Ingested [The DeepMind Institute: Foundational Research, AGI Governance & Inaugural Essays](/ecosystem/institutions/deepmind-institute.md) from [DeepMind Institute](https://institute.deepmind.com/#essays) synthesizing the Institute's founding charter, governance model, and all eight inaugural essays on agent swarms, symbiotic intelligence, reasoning transparency, global benefit, and AGI economic policy.
* **Skill Upgrades**: Enhanced [`/ingest`](/skills/ingest/SKILL.md), [`/manage-knowledge-base`](/skills/manage-knowledge-base/SKILL.md), [`/ask-kb`](/skills/ask-kb/SKILL.md), and [`AGENTS.md`](/AGENTS.md) with dedicated support for ingesting institutional portals, publication series, multi-essay dossiers, and automatic registration in the Institutions Observatory.
* **Institution Template**: Added [`templates/institution-template.md`](/templates/institution-template.md) and [`skills/manage-knowledge-base/templates/institution_template.md`](/skills/manage-knowledge-base/templates/institution_template.md) providing a standardized structure for profiling external AI institutes, frontier labs, and moral authorities.
* **Institutional Expansion**: Ingested comprehensive dossiers into the Global AI Institutions Observatory covering:
  * [Harvard Human Flourishing Program](/ecosystem/institutions/harvard-human-flourishing.md): Empirical research on character, eudaimonia, well-being domains, and critique of synthetic intimacy.
  * [UN High-Level Advisory Body on AI](/ecosystem/institutions/un-ai-advisory-body.md): September 2024 final report *Governing AI for Humanity*, establishing 7 structural pillars to bridge the global governance deficit.
  * [Council of Europe AI Framework Convention](/ecosystem/institutions/council-of-europe-ai.md): The world's first legally binding international treaty on AI (CETS No. 225) protecting human rights, democracy, and rule of law.
  * [Rome Call for AI Ethics & Hiroshima Appeal](/ecosystem/institutions/rome-call-hiroshima.md): July 2024 historic expansion of algor-ethics to Eastern religions and categorical moral ban on lethal autonomous weapons.
  * [Oxford Institute for Ethics in AI](/ecosystem/institutions/oxford-ethics-ai.md): Aristotelian virtue ethics, HAI Lab, and the landmark *Positive Alignment* research agenda for human flourishing.
* **Template Cleanup**: Removed obsolete starter template files (`concepts/future-initiative.md`, `systems/core-architecture.md`, `ecosystem/industry-landscape.md`), personalized `knowledge.config.json` for St. Francis High School's AI Initiative, and retained `research/user-interview-example.md` as an exemplar for Human-Centered Design (HCD) research.

## 2026-09-26
* **Agent Guidelines**: Added [`AGENTS.md`](/AGENTS.md) repository-wide operating contract for autonomous AI agents.
* **Knowledge Advisor Skill**: Added [`/ask-kb`](/skills/ask-kb/SKILL.md) and [`scripts/query_kb.py`](/scripts/query_kb.py) CLI & programmatic search tool.
* **Knowledge-Driven Engineering**: Added [`playbooks/knowledge-driven-engineering.md`](/playbooks/knowledge-driven-engineering.md) defining spec-driven development, AI pair programming, compliance PR reviews, and concept graduation.
* **Repository Initialized**: Extracted self-contained, self-maintaining knowledge base template conforming to Google OKF v0.2.
* **Architecture Groundwork**: Established core taxonomies across `/systems/`, `/ecosystem/`, `/concepts/`, `/playbooks/`, `/research/`, and `/references/`.
* **Tooling Configured**: Automated presubmit gatekeeper, bundle validator, and dynamic index generator verified.
