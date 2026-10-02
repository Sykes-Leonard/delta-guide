---
okf_version: "0.2"
title: "St. Francis High School AI Initiative Knowledge Base"
description: "Canonical Open Knowledge Format (OKF v0.2) knowledge base for the St. Francis High School AI Initiative, integrating the DELTA Framework, Magnifica Humanitas, and Human-Centered Design (HCD) research."
---

# St. Francis High School AI Initiative Knowledge Base

Canonical Open Knowledge Format (OKF v0.2) knowledge base for the St. Francis High School AI Initiative, integrating the DELTA Framework, Magnifica Humanitas, and Human-Centered Design (HCD) research.

Knowledge in this bundle is organized with clear demarcation between:
1. **"What Is"**: Operational realities, external ecosystem context (`/ecosystem/`), and active production systems (`/systems/`).
2. **"What Could Be"**: Future proposals, feature specifications, and architectural explorations (`/concepts/`).
3. **"How To" & Provenance**: Operational runbooks (`/playbooks/`), field research (`/research/`), and standards (`/references/`).

---

## External Ecosystem & Industry Reality ('What Is')

* [The DELTA Framework: Faith-Informed Virtue Ethics for Artificial Intelligence](/ecosystem/delta-framework.md) - Notre Dame's virtue-ethics framework establishing five core normative pillars—Dignity, Embodiment, Love, Transcendence, and Agency—and practical tools for human formation in the AI era.
* [Encyclical Letter Magnifica Humanitas: Safeguarding the Human Person in the Time of Artificial Intelligence](/ecosystem/magnifica-humanitas.md) - Pope Leo XIV's landmark 2026 social encyclical on artificial intelligence, addressing private technocratic dominance, algorithmic reductionism, the dignity of labor, and autonomous warfare.

## Operational Playbooks & Runbooks

* [Knowledge-Driven Engineering & Spec-Driven Development](/playbooks/knowledge-driven-engineering.md) - Comprehensive operational playbook for integrating the knowledge base into sprint planning, coding, AI pair programming, pull request compliance reviews, and living documentation graduation.
* [Developer & Contributor Onboarding Guide](/playbooks/onboarding-guide.md) - Step-by-step instructions for engineers and AI agents to set up local environments, verify builds, and run tests.

## Field Research & User Interviews

* [Customer Discovery & Workflow Observations](/research/user-interview-example.md) - Field interview and observation notes exploring user workflow friction and queue management pain points.

## Agent Skills & Automation Capabilities

* [Knowledge Base Advisor (/ask-kb)](/skills/ask-kb/SKILL.md) - Provides instant, authoritative domain and architectural consulting across production systems, external ecosystems, and product concepts. Use when developers or AI agents need domain context, schema contracts, or compliance guidance.
* [Ingest URL Content into Knowledge Base](/skills/ingest/SKILL.md) - Downloads external web content from a URL, analyzes its relevance to the organization, asks the user for placement confirmation, and synthesizes it into an OKF v0.2 knowledge document.
* [Article or Policy Title](/skills/ingest/templates/ingested-source-template.md) - Single-sentence executive summary of the ingested document and its organizational relevance.
* [Manage Knowledge Base (OKF v0.2)](/skills/manage-knowledge-base/SKILL.md) - Navigate, read, author, update, and validate the markdown knowledge base according to Google OKF v0.2.
* [Google OKF v0.2 Quick Reference Cheat Sheet](/skills/manage-knowledge-base/references/okf_cheat_sheet.md) - Reference cheat sheet for Open Knowledge Format frontmatter fields and conventions.
* [Concept Template](/skills/manage-knowledge-base/templates/concept_template.md) - Starter template for proposing a new feature or architectural RFC.
* [Interview / Field Notes Template](/skills/manage-knowledge-base/templates/interview_template.md) - Starter template for recording qualitative customer research and provenance.
* [Playbook Template](/skills/manage-knowledge-base/templates/playbook_template.md) - Starter template for an operational runbook or SOP.

## Standards, Specifications & References

* [Google Open Knowledge Format Specification](/references/okf-specification.md) - Canonical summary of the Google OKF v0.2 specification, trust tiers, and conventions.
* [Knowledge Provenance & Lineage Guidelines](/references/provenance.md) - Guidelines and architecture for tracking source lineage, citations, and trust verification across the knowledge base.
* [Bundle Update Log](/log.md) - Chronological record of additions, modifications, and verifications in this bundle.

## Knowledge Document Starter Templates

* [Concept Template](/templates/concept-template.md) - Starter template for proposing a new product feature, architectural RFC, or exploratory innovation ('What Could Be').
* [Ecosystem Context Template](/templates/ecosystem-template.md) - Starter template for documenting external infrastructure, regulatory requirements, partner platforms, and market realities ('What Is').
* [Playbook Template](/templates/playbook-template.md) - Starter template for standard operating procedures, developer setups, incident guides, and team runbooks.
* [Technical Reference Template](/templates/reference-template.md) - Starter template for specifications, protocol data dictionaries, and architectural standards.
* [Research Notes Template](/templates/research-template.md) - Starter template for customer interviews, field observations, and user research.
* [System Component Template](/templates/system-template.md) - Starter template for documenting active production software, backend services, or data architectures ('What Is').

## General Documents

* [AI Agent Guidelines & Operating Contract](/AGENTS.md) - Repository-level operating rules and architectural constraints for AI agents interacting with this codebase and knowledge base.
* [Knowledge Guide Starter Template (Google OKF v0.2)](/README.md) - A turnkey, self-contained, and self-maintaining knowledge base template for engineering, product, and operational teams.
* [Knowledge Guide Setup & Onboarding Guide (Human & AI Agent Instructions)](/SETUP.md) - Idempotent, step-by-step instructions for humans and autonomous AI agents to clone, configure, personalize, and verify the OKF v0.2 knowledge base.
