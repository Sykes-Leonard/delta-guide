---
type: Playbook
title: "Antigravity Onboarding & Test Drive Playbook"
description: "Step-by-step instructions for installing Antigravity (Free), configuring the workspace, and testing agent skills and knowledge."
tags: [playbook, antigravity, quickstart, testing, skills, okf]
status: stable
generated:
  by: agent:antigravity
  at: 2026-10-02T00:00:00Z
verified:
  - by: human:architecture-lead
    at: 2026-10-02T00:00:00Z
sources:
  - "https://antigravity.google/docs"
  - "https://antigravity.google/cli/install.sh"
---

# Antigravity Onboarding & Test Drive Playbook

## 1. Purpose & Scope

This playbook guides engineers, architects, and researchers through installing the free edition of **Google Antigravity**, cloning this repository, and immediately executing autonomous knowledge queries, web ingestion, and presubmit validation workflows.

---

## 2. Installing Google Antigravity (Free Desktop Application)

The **Google Antigravity** desktop application is an agent-first platform that lets you pair-program with AI agents to orchestrate multi-step tasks, execute terminal commands, view interactive artifacts, and maintain repository integrity.

### Installation Steps

1. **Download the Application**:
   * **Direct Installer**: Download the installer for your OS from [antigravity.google/download](https://antigravity.google/download).
   * **macOS Homebrew**:
     ```bash
     brew install --cask antigravity
     ```

2. **Authenticate with Google (Free)**:
   Launch Antigravity from `/Applications/Antigravity.app`. Sign in with your standard Google account (no paid Vertex AI project or credit card required for the free tier).

3. **Open this Repository as a Project**:
   * In Antigravity's left-hand sidebar, click **Projects** $\rightarrow$ **Open Project** (or use `File -> Open Folder`) and choose `delta-guide`.
   * Or from the terminal:
     ```bash
     open -a Antigravity /path/to/delta-guide
     ```

---

## 3. The Antigravity Desktop Interface Surfaces

When you open this repository in Antigravity, you interact through three unified surfaces:

1. **Left-hand Sidebar**:
   * **New Conversation**: Start a fresh agent chat session.
   * **Projects**: Switch between workspaces.
   * **Skills & Customizations**: View the active workspace skills mounted from `.agents/skills`.
2. **Chat Canvas (Center)**:
   * The primary interaction canvas where you type instructions or invoke slash commands (e.g., `/ask-kb`).
   * Type `@` to attach specific files, folders, or terminal context.
3. **Auxiliary Pane (Right)**:
   * Displays live **Artifacts**, diff views, terminal executions, and subagent transcripts as the agent works.

---

## 4. Workspace Configuration & Agent Discovery

When Antigravity opens this repository, it automatically reads:
1. **`AGENTS.md`**: The repository-level operating contract that governs how agents query domain truth, protect data privacy, and maintain progressive disclosure.
2. **`.agents/skills/`**: The registered agent skills mounted in the workspace:
   - `/ask-kb`: Instant vectorless domain consulting.
   - `/ingest`: Autonomous web scraper, classifier, and OKF document generator.
   - `/manage-knowledge-base`: Navigation, authoring, and audit tool for OKF v0.2 documents.
   - `/generate-storyboards`: Multi-panel visual storyboard and product concept generator.
   - `/backout-institution` & `/backout-source`: Safe decoupling tools for knowledge graphs.

Run `./setup.sh` (or `./quickstart.sh`) to ensure file permissions and Git presubmit hooks are configured:
```bash
./setup.sh
```

---

## 5. The 4 Golden Test-Drive Prompts

Once Antigravity is open in your terminal or IDE, test out the knowledge base by running these 4 exercises:

### Test 1: Vectorless Knowledge Retrieval (`/ask-kb`)
*Prompt to send the agent:*
```text
/ask-kb What is the DELTA framework and what virtues does it evaluate?
```
**Expected Behavior**:
The agent invokes the `ask-kb` skill, which executes `scripts/query_kb.py` to perform BM25-style keyword search over the structured markdown corpus. It synthesizes an authoritative summary citing exact lines from `/ecosystem/delta-framework.md`.

---

### Test 2: Progressive Disclosure Traversal
*Prompt to send the agent:*
```text
Summarize the high-level ecosystem realities and production systems in index.md.
```
**Expected Behavior**:
The agent reads `/index.md` first, scanning the one-line summaries across categories without wasting context on dozens of detailed files, demonstrating efficient agent navigation.

---

### Test 3: Autonomous Web Ingestion (`/ingest`)
*Prompt to send the agent:*
```text
/ingest https://en.wikipedia.org/wiki/Virtue_ethics
```
**Expected Behavior**:
The agent downloads the external URL, extracts core definitions, interactively consults with you on placement within the knowledge taxonomy, generates a validated OKF v0.2 markdown file, updates `log.md`, and runs the presubmit check.

---

### Test 4: Self-Healing Presubmit Gatekeeper
*Prompt to send the agent:*
```text
Draft a new concept document for an "Autonomous Compliance Auditor" in concepts/ and run presubmit validation.
```
**Expected Behavior**:
The agent creates the draft, adds frontmatter with `status: draft`, specifies typed relational edges, updates a cluster matrix, and runs `./scripts/presubmit.py`. The gatekeeper validates link integrity, schema conformance, and re-indexes `index.md`.

---

## 6. Verification Checklist

To confirm your installation and repository readiness:

```bash
# 1. Verify bundle integrity and presubmit gatekeeper
python3 scripts/presubmit.py
# Must return: "Result: PASSED ✅ (Fully conformant with OKF v0.2)"

# 2. Test CLI search
python3 scripts/query_kb.py "virtue ethics"

# 3. Verify agent discovery
test -d .agents/skills && echo "✓ Agent skills mounted"
```
