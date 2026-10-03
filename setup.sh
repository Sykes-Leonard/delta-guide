#!/usr/bin/env bash
# ==============================================================================
# setup.sh - Environment Setup & Presubmit Hook Installer (OKF v0.2)
# ==============================================================================
# Verifies system prerequisites, installs Git pre-commit & pre-push hooks,
# configures AI agent discovery (.agents/skills.json), and executes a bundle
# self-test validation to ensure the knowledge base is fully self-maintaining.
# ==============================================================================

set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "\n${BOLD}${BLUE}============================================================${NC}"
echo -e "${BOLD}${BLUE}  Knowledge Guide (OKF v0.2) Setup & Validation Checker     ${NC}"
echo -e "${BOLD}${BLUE}============================================================${NC}\n"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. Detect Operating System
OS="$(uname -s)"
echo -e "${BLUE}[1/7]${NC} Detecting operating system: ${GREEN}$OS${NC}"

# 2. Check for Python 3 (Requirement: Python 3.8+)
echo -e "\n${BLUE}[2/7]${NC} Checking for Python 3 (required: >= 3.8)..."
PYTHON_BIN=""
if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null && python --version 2>&1 | grep -q "Python 3"; then
    PYTHON_BIN="python"
fi

if [ -z "$PYTHON_BIN" ]; then
    echo -e "      ${RED}Error: Python 3 not found.${NC} Please install Python 3.8+."
    exit 1
fi

PY_VERSION="$($PYTHON_BIN -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')"
echo -e "      Found: ${GREEN}$PYTHON_BIN ($PY_VERSION)${NC}"

PY_CHECK="$($PYTHON_BIN -c 'import sys; print(1 if sys.version_info >= (3, 8) else 0)')"
if [ "$PY_CHECK" -ne 1 ]; then
    echo -e "      ${RED}Error:${NC} Python 3.8 or higher is required. Found $PY_VERSION."
    exit 1
fi

# 3. Check Version Control Tooling (Git / Jujutsu)
echo -e "\n${BLUE}[3/7]${NC} Checking version control tooling..."
if command -v git &>/dev/null; then
    GIT_VER="$(git --version)"
    echo -e "      ${GREEN}✓${NC} Git found: ${GREEN}$GIT_VER${NC}"
fi

if command -v jj &>/dev/null; then
    JJ_VER="$(jj version | head -n 1)"
    echo -e "      ${GREEN}✓${NC} Jujutsu (jj) found: ${GREEN}$JJ_VER${NC}"
else
    echo -e "      ${YELLOW}!${NC} Jujutsu (jj) optional modern VCS not detected."
fi

# 4. Check for Google Antigravity (Free Agentic Development Platform)
echo -e "\n${BLUE}[4/7]${NC} Checking for Google Antigravity (CLI / IDE)..."
AGY_DETECTED=0
if command -v agy &>/dev/null; then
    AGY_VER="$(agy --version 2>/dev/null || echo "detected")"
    echo -e "      ${GREEN}✓${NC} Antigravity CLI (agy) found: ${GREEN}$AGY_VER${NC}"
    AGY_DETECTED=1
elif [ -f "$HOME/.local/bin/agy" ]; then
    echo -e "      ${GREEN}✓${NC} Antigravity CLI (agy) found at ${GREEN}$HOME/.local/bin/agy${NC}"
    AGY_DETECTED=1
fi

if [ -d "/Applications/Antigravity.app" ] || [ -d "$HOME/Applications/Antigravity.app" ]; then
    echo -e "      ${GREEN}✓${NC} Antigravity Desktop IDE found in Applications"
    AGY_DETECTED=1
elif command -v antigravity &>/dev/null; then
    echo -e "      ${GREEN}✓${NC} Antigravity IDE found in PATH"
    AGY_DETECTED=1
fi

if [ "$AGY_DETECTED" -eq 0 ]; then
    echo -e "      ${YELLOW}!${NC} Antigravity not detected (optional, but recommended to interact with this guide)."
    echo -e "        • Install CLI (Free):      ${BOLD}curl -fsSL https://antigravity.google/cli/install.sh | bash${NC}"
    echo -e "        • Download IDE (Free):     ${BOLD}https://antigravity.google/download${NC}"
    if [ -t 0 ] && [ "${CI:-false}" != "true" ]; then
        echo -ne "        Would you like to install Antigravity CLI now? [y/N]: "
        read -r install_agy || install_agy="n"
        if [[ "$install_agy" =~ ^[Yy]$ ]]; then
            echo -e "        Installing Antigravity CLI..."
            curl -fsSL https://antigravity.google/cli/install.sh | bash || true
            if [ -f "$HOME/.local/bin/agy" ]; then
                export PATH="$HOME/.local/bin:$PATH"
                echo -e "        ${GREEN}✓${NC} Antigravity CLI installed successfully!"
            fi
        fi
    fi
fi

# 5. Ensure Permissions on Maintenance and Skill Scripts & Install Git Hooks
echo -e "\n${BLUE}[5/7]${NC} Setting script permissions and configuring presubmit hooks..."
chmod +x init.sh 2>/dev/null || true
chmod +x quickstart.sh 2>/dev/null || true
if [ -d "scripts" ]; then
    chmod +x scripts/*.py 2>/dev/null || true
    echo -e "      ${GREEN}✓${NC} scripts/*.py are executable"
fi

if [ -d "skills" ]; then
    find skills -type f -name "*.py" -exec chmod +x {} + 2>/dev/null || true
    echo -e "      ${GREEN}✓${NC} skills/**/scripts/*.py are executable"
fi

# Configure Git hooks if .git directory exists
if [ -d ".git" ]; then
    mkdir -p .git/hooks

    # Install git pre-commit hook
    cat << 'EOF' > .git/hooks/pre-commit
#!/usr/bin/env bash
set -euo pipefail
GIT_DIR="$(git rev-parse --git-dir)"
REPO_ROOT="$(cd "$GIT_DIR/.." && pwd)"
PYTHON_BIN=""
if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    PYTHON_BIN="python"
else
    echo "ERROR: python3 not found. Presubmit hook cannot run." >&2
    exit 1
fi
exec "$PYTHON_BIN" "$REPO_ROOT/scripts/presubmit.py" "$REPO_ROOT"
EOF
    chmod +x .git/hooks/pre-commit

    # Install git pre-push hook
    cat << 'EOF' > .git/hooks/pre-push
#!/usr/bin/env bash
set -euo pipefail
GIT_DIR="$(git rev-parse --git-dir)"
REPO_ROOT="$(cd "$GIT_DIR/.." && pwd)"
PYTHON_BIN=""
if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    PYTHON_BIN="python"
else
    echo "ERROR: python3 not found. Presubmit hook cannot run." >&2
    exit 1
fi
exec "$PYTHON_BIN" "$REPO_ROOT/scripts/presubmit.py" "$REPO_ROOT"
EOF
    chmod +x .git/hooks/pre-push
    echo -e "      ${GREEN}✓${NC} Installed OKF presubmit hooks in .git/hooks/ (pre-commit, pre-push)"
else
    echo -e "      ${YELLOW}!${NC} .git directory not found (hooks will install when git init is run)"
fi

# 6. Verify Agent Discovery Configuration
echo -e "\n${BLUE}[6/7]${NC} Verifying AI agent workspace discovery configuration..."
mkdir -p .agents
if [ ! -f ".agents/skills.json" ]; then
    cat << 'EOF' > .agents/skills.json
{
  "skills": [
    { "path": "skills" }
  ]
}
EOF
    echo -e "      ${GREEN}✓${NC} Created .agents/skills.json"
else
    echo -e "      ${GREEN}✓${NC} .agents/skills.json exists"
fi

if [ -d "skills" ] && [ ! -e ".agents/skills" ]; then
    ln -sfn ../skills .agents/skills
    echo -e "      ${GREEN}✓${NC} Linked .agents/skills -> ../skills"
fi

# 7. Run Self-Test Validation & Re-indexing
echo -e "\n${BLUE}[7/7]${NC} Running self-test presubmit validation on OKF bundle..."
if $PYTHON_BIN scripts/presubmit.py; then
    echo -e "${BOLD}${GREEN}============================================================${NC}"
    echo -e "${BOLD}${GREEN}  Setup Complete! Knowledge Base is Operational & Verified   ${NC}"
    echo -e "${BOLD}${GREEN}============================================================${NC}"
    echo -e "\nQuick Run Commands:"
    echo -e "  • Launch Antigravity:  ${BOLD}agy${NC} (or open folder in Antigravity IDE)"
    echo -e "  • Test Drive Prompts:  ${BOLD}cat playbooks/antigravity-test-drive.md${NC}"
    echo -e "  • Personalize / Brand: ${BOLD}./init.sh --org \"My Org\"${NC}"
    echo -e "  • Presubmit Check:     ${BOLD}./scripts/presubmit.py${NC} (auto-fix + validate)"
    echo -e "  • Validate Bundle:     ${BOLD}./scripts/validate.py${NC} (or ${BOLD}./scripts/validate.py --fix${NC})"
    echo -e "  • Refresh Index:       ${BOLD}./scripts/update_index.py${NC}"
    echo -e "  • Search Knowledge:    ${BOLD}./scripts/query_kb.py \"<query>\"${NC}\n"
    exit 0
else
    echo -e "\n${BOLD}${RED}Validation Failed. Please review errors above.${NC}\n"
    exit 1
fi
