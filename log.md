# Knowledge Base Changelog

## 2026-10-01
* **Source Retraction & Decoupler Engine**: Added [`scripts/backout_source.py`](/scripts/backout_source.py), [`scripts/backout_institution.py`](/scripts/backout_institution.py), [`scripts/reincorporate_source.py`](/scripts/reincorporate_source.py), and autonomous agent skills [`/backout-source`](/skills/backout-source/SKILL.md) and [`/backout-institution`](/skills/backout-institution/SKILL.md) for safely auditing, retracting, archiving, substituting, and restoring external sources and institutional containers.
* **Concept Graph & Relational Edge Engine**: Enhanced [`scripts/validate.py`](/scripts/validate.py) with `validate_concept_graph()` to verify cluster membership, typed relational edges, and source provenance, while exempting `archive/` and hidden directories from presubmit.
* **Ontology & Taxonomy Demarcation**: Formally expanded OKF layout into a 3-tier ontological separation: "What Is" (`/systems/`, `/ecosystem/`, `/ecosystem/institutions/`), "Theoretical Frameworks" (`/concepts/`), and "What Could Be" (`/frontier/`, `/storyboards/`).
* **Authoring Templates & Observatories**: Added [`templates/concept-cluster-template.md`](/templates/concept-cluster-template.md), [`templates/frontier-template.md`](/templates/frontier-template.md), and [`templates/institution-template.md`](/templates/institution-template.md).
* **Obsidian Graph Optimization**: Added [`.obsidian/graph.json`](/.obsidian/graph.json) with tuned graph physics for knowledge base visualization.

## 2026-09-30
* **Storyboarding Skill**: Added [`/generate-storyboards`](/skills/generate-storyboards/SKILL.md) skill, [`templates/storyboard-template.md`](/templates/storyboard-template.md), and [`playbooks/generating-product-storyboards.md`](/playbooks/generating-product-storyboards.md) for authoring sequential visual storyboards and product concept specifications.

## 2026-09-26
* **Agent Guidelines**: Added [`AGENTS.md`](/AGENTS.md) repository-wide operating contract for autonomous AI agents.
* **Knowledge Advisor Skill**: Added [`/ask-kb`](/skills/ask-kb/SKILL.md) and [`scripts/query_kb.py`](/scripts/query_kb.py) CLI & programmatic search tool.
* **Knowledge-Driven Engineering**: Added [`playbooks/knowledge-driven-engineering.md`](/playbooks/knowledge-driven-engineering.md) defining spec-driven development, AI pair programming, compliance PR reviews, and concept graduation.
* **Repository Initialized**: Extracted self-contained, self-maintaining knowledge base template conforming to Google OKF v0.2.
* **Architecture Groundwork**: Established core taxonomies across `/systems/`, `/ecosystem/`, `/concepts/`, `/playbooks/`, `/research/`, and `/references/`.
* **Tooling Configured**: Automated presubmit gatekeeper, bundle validator, and dynamic index generator verified.
