---
type: Playbook
title: "Developer & Contributor Onboarding Guide"
description: "Step-by-step instructions for engineers and AI agents to set up local environments, verify builds, and run tests."
tags: [playbook, onboarding, developer, setup]
status: stable
generated:
  by: agent:antigravity
  at: 2026-09-26T00:00:00Z
verified:
  - by: human:lead-engineer
    at: 2026-09-26T00:00:00Z
---

# Developer & Contributor Onboarding Guide

## 1. Purpose & Scope
This playbook provides an idempotent, step-by-step checklist for new engineers and autonomous AI agents joining the team. Following these steps ensures your local development workstation is fully configured, verified, and ready to contribute.

---

## 2. Prerequisites
Ensure the host machine satisfies:
* **Operating System**: macOS (12+) or Linux (Ubuntu 20.04+, Debian 11+, Fedora 36+)
* **Python**: Version 3.8 or higher (`python3 --version`)
* **Git**: Version 2.20 or higher (`git --version`)
* *(Optional)* **Jujutsu (`jj`)**: Modern version control tool (`jj --version`)

---

## 3. Step-by-Step Setup

### Step 1: Clone and Configure Knowledge Base
```bash
git clone <repository_url>
cd <repository_directory>
./setup.sh
```

### Step 2: Verify Presubmit Gatekeeper
The presubmit script validates that all documents adhere to OKF v0.2 and fixes any minor formatting issues automatically:
```bash
python3 scripts/presubmit.py
```

### Step 3: Run Test Suite
Verify that local tests and linters pass cleanly:
```bash
./scripts/validate.py
```

---

## 4. Operational Best Practices
* **Keep Knowledge Fresh**: Whenever you implement a new feature or change an API, update the corresponding file in `/systems/` or `/concepts/`.
* **Run Presubmit Before Push**: Git hooks are pre-installed by `./setup.sh`, but you can always run `./scripts/presubmit.py` manually.
