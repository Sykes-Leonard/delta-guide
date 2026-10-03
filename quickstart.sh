#!/usr/bin/env bash
# ==============================================================================
# quickstart.sh - 1-Minute Antigravity & Knowledge Guide Quickstart
# ==============================================================================
# Automates environment setup, checks/installs Antigravity (Free Edition),
# verifies bundle integrity with presubmit, and launches the agent test drive.
# ==============================================================================

set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "\n${BOLD}${CYAN}============================================================${NC}"
echo -e "${BOLD}${CYAN}   Google Antigravity + Knowledge Guide Quickstart 🚀       ${NC}"
echo -e "${BOLD}${CYAN}============================================================${NC}\n"

# 1. Run standard idempotent setup (environment, permissions, hooks, bundle test)
./setup.sh

# 2. Check if agy binary is in PATH or standard user install paths
if ! command -v agy &>/dev/null; then
    if [ -f "$HOME/.local/bin/agy" ]; then
        export PATH="$HOME/.local/bin:$PATH"
    fi
fi

# 3. Present the 4 Golden Test-Drive Prompts
echo -e "\n${BOLD}${CYAN}============================================================${NC}"
echo -e "${BOLD}${CYAN}   Ready for Testing! 4 Golden Prompts to Try               ${NC}"
echo -e "${BOLD}${CYAN}============================================================${NC}\n"
echo -e "Once Antigravity starts, paste any of these prompts into the chat:\n"
echo -e "  ${BOLD}1. Domain Knowledge Retrieval:${NC}"
echo -e "     ${CYAN}/ask-kb What is the DELTA framework and what virtues does it evaluate?${NC}\n"
echo -e "  ${BOLD}2. Progressive Disclosure Exploration:${NC}"
echo -e "     ${CYAN}Summarize the core systems and ecosystem realities outlined in index.md${NC}\n"
echo -e "  ${BOLD}3. Autonomous Web Ingestion:${NC}"
echo -e "     ${CYAN}/ingest https://en.wikipedia.org/wiki/Virtue_ethics${NC}\n"
echo -e "  ${BOLD}4. Self-Healing Quality Gatekeeper:${NC}"
echo -e "     ${CYAN}Draft a new concept for an Autonomous Compliance Auditor and verify with presubmit${NC}\n"
echo -e "------------------------------------------------------------"

if command -v agy &>/dev/null; then
    if [ -t 0 ] && [ "${CI:-false}" != "true" ]; then
        echo -ne "\n${BOLD}Would you like to launch Antigravity CLI (agy) now? [Y/n]: ${NC}"
        read -r launch_agy || launch_agy="y"
        if [[ "$launch_agy" =~ ^[Yy]$ ]] || [ -z "$launch_agy" ]; then
            echo -e "\n${GREEN}Starting Antigravity CLI... (Type /exit or Ctrl+D Ctrl+D to quit)${NC}\n"
            exec agy
        fi
    else
        echo -e "\nLaunch the Antigravity CLI at any time with: ${BOLD}agy${NC}"
    fi
else
    echo -e "\nTo launch the Antigravity Desktop IDE, open this directory:"
    echo -e "  ${BOLD}$SCRIPT_DIR${NC} in Antigravity IDE (download: https://antigravity.google/download)"
    echo -e "Or install the lightweight CLI via:"
    echo -e "  ${BOLD}curl -fsSL https://antigravity.google/cli/install.sh | bash${NC}\n"
fi
