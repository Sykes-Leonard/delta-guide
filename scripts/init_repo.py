#!/usr/bin/env python3
"""
init_repo.py - Fast onboarding and personalization script for new organizations.

Customizes organization name, titles, descriptions, and regenerates index and configuration.
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from update_index import generate_index
from validate import validate_bundle

def customize_repo(repo_dir: Path, org_name: str, kb_title: str, kb_desc: str):
    print(f"⚙️  Customizing Knowledge Guide for: {org_name}...\n")
    
    # 1. Update knowledge.config.json
    cfg_file = repo_dir / "knowledge.config.json"
    cfg = {}
    if cfg_file.exists():
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            pass
            
    cfg["org_name"] = org_name
    cfg["kb_title"] = kb_title
    cfg["kb_description"] = kb_desc
    
    with open(cfg_file, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    print("  ✔ Updated knowledge.config.json")
    
    # 2. Update README.md title if template placeholder exists
    readme_file = repo_dir / "README.md"
    if readme_file.exists():
        content = readme_file.read_text(encoding="utf-8")
        content = content.replace("Example Organization", org_name)
        content = content.replace("Organization Knowledge Base", kb_title)
        readme_file.write_text(content, encoding="utf-8")
        print("  ✔ Updated README.md")
        
    # 3. Update SETUP.md title if template placeholder exists
    setup_file = repo_dir / "SETUP.md"
    if setup_file.exists():
        content = setup_file.read_text(encoding="utf-8")
        content = content.replace("Example Organization", org_name)
        content = content.replace("Organization Knowledge Base", kb_title)
        setup_file.write_text(content, encoding="utf-8")
        print("  ✔ Updated SETUP.md")
        
    # 4. Append to log.md
    log_file = repo_dir / "log.md"
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log_entry = f"## {today_str}\n* **Initialization**: Configured knowledge base template for **{org_name}**.\n\n"
    if log_file.exists():
        existing_log = log_file.read_text(encoding="utf-8")
        if not existing_log.startswith(f"## {today_str}"):
            log_file.write_text(log_entry + existing_log, encoding="utf-8")
        else:
            # Append under existing date heading
            lines = existing_log.splitlines(True)
            lines.insert(1, f"* **Initialization**: Configured knowledge base template for **{org_name}**.\n")
            log_file.write_text("".join(lines), encoding="utf-8")
    else:
        log_file.write_text(f"# Knowledge Base Changelog\n\n{log_entry}", encoding="utf-8")
    print("  ✔ Logged initialization event in log.md")
    
    # 5. Regenerate index.md
    generate_index(repo_dir)
    print("  ✔ Regenerated root index.md")
    
    # 6. Validate and auto-fix
    print("\n🔍 Validating bundle health...")
    ret = validate_bundle(repo_dir, fix=True)
    if ret == 0:
        print(f"\n🎉 Successfully initialized knowledge guide for {org_name}!")
        print("Next steps:")
        print("  1. Review knowledge.config.json for customized categories.")
        print("  2. Run ./setup.sh to install presubmit git hooks & agent discovery.")
        print("  3. Begin authoring in systems/, ecosystem/, concepts/, and playbooks/.")
    return ret

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize knowledge base for your organization.")
    parser.add_argument("--org", type=str, help="Organization Name (e.g. Acme Health)")
    parser.add_argument("--title", type=str, help="Knowledge Base Title (e.g. Acme Knowledge Guide)")
    parser.add_argument("--desc", type=str, help="Single-sentence summary of the knowledge base")
    parser.add_argument("--repo-dir", type=Path, default=REPO_ROOT, help="Knowledge base root path")
    args = parser.parse_args()
    
    org = args.org
    if not org and sys.stdin.isatty():
        try:
            org = input("Enter your organization name [Example Organization]: ").strip()
        except EOFError:
            pass
    if not org:
        org = "Example Organization"
        
    title = args.title
    if not title:
        title = f"{org} Knowledge Base"
        
    desc = args.desc
    if not desc:
        desc = f"Canonical Open Knowledge Format (OKF v0.2) knowledge base for {org}."
        
    sys.exit(customize_repo(args.repo_dir, org, title, desc))
