#!/usr/bin/env python3
"""
presubmit.py - OKF Knowledge Base Presubmit Hook & Gatekeeper.

Enforces knowledge base integrity prior to commit or push:
1. Runs automated fixing (--fix) across all markdown concepts and reserved files.
2. Synchronizes root index.md from concept frontmatter.
3. Automatically stages any repaired files if running within a git commit hook context.
4. Validates full bundle conformance to Google OKF v0.2.
5. Blocks commits/pushes if unresolvable errors remain.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Add scripts directory to path to import validate
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from validate import validate_bundle

def is_git_repo(path: Path) -> bool:
    try:
        res = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return res.returncode == 0 and res.stdout.strip() == "true"
    except Exception:
        return False

def get_staged_files(repo_dir: Path) -> list:
    try:
        res = subprocess.run(
            ["git", "-C", str(repo_dir), "diff", "--cached", "--name-only"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if res.returncode == 0:
            return [line.strip() for line in res.stdout.splitlines() if line.strip()]
    except Exception:
        pass
    return []

def get_modified_files(repo_dir: Path) -> list:
    try:
        res = subprocess.run(
            ["git", "-C", str(repo_dir), "diff", "--name-only"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if res.returncode == 0:
            return [line.strip() for line in res.stdout.splitlines() if line.strip()]
    except Exception:
        pass
    return []

def run_presubmit(bundle_dir: Path, check_only: bool = False) -> int:
    print("🚀 Running OKF v0.2 Presubmit Gatekeeper...\n")
    
    in_git = is_git_repo(bundle_dir)
    staged_before = get_staged_files(bundle_dir) if in_git else []
    
    # Run validation (with auto-fixing unless explicitly check_only)
    fix_enabled = not check_only
    ret = validate_bundle(bundle_dir, fix=fix_enabled)
    
    # Re-compile viewer graph data
    try:
        from compile_graph import compile_graph
        compile_graph(bundle_dir, bundle_dir / "viewer" / "graph-data.json")
    except Exception as e:
        print(f"Warning: Failed to compile viewer graph data: {e}")

    # If in git and files were already staged for commit, stage any newly fixed files
    if in_git and staged_before and fix_enabled:
        modified_after = get_modified_files(bundle_dir)
        to_stage = [f for f in modified_after if f.endswith(".md") or f.endswith(".py") or f.endswith(".json")]
        if to_stage:
            print(f"📦 Staging {len(to_stage)} auto-repaired file(s) for git commit:")
            for f in to_stage:
                print(f"   + git add {f}")
            subprocess.run(["git", "-C", str(bundle_dir), "add"] + to_stage, check=False)
            print()
            
    if ret == 0:
        print("✅ Presubmit Passed: Knowledge Base is verified & conformant.\n")
    else:
        print("❌ Presubmit Failed: Please resolve the errors listed above before committing.\n")
        
    return ret

if __name__ == "__main__":
    default_bundle_root = SCRIPT_DIR.parent
    parser = argparse.ArgumentParser(description="OKF v0.2 Presubmit Validator & Auto-fixer")
    parser.add_argument("bundle_root", nargs="?", default=default_bundle_root, type=Path, help="Bundle directory root")
    parser.add_argument("--check-only", action="store_true", help="Run validation without applying auto-fixes")
    args = parser.parse_args()
    
    sys.exit(run_presubmit(args.bundle_root, check_only=args.check_only))
