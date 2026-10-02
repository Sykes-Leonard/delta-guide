#!/usr/bin/env python3
"""
reincorporate_source.py - OKF Source & Concept Archive Reincorporator.

Restores backed-out sources, pruned concepts, and institutions from the archive/ folder
back into the active knowledge graph:
1. Reincorporates deleted files from archive/<id>/files/.
2. Restores source citations to multi-grounded concepts.
3. Restores concept rows to parent cluster matrices.
4. Restores reciprocal edges to peer concept tables.
5. Restores institution rows to ecosystem/institutions/overview.md.
6. Records reincorporation in log.md and runs the presubmit gatekeeper.
"""

import sys
import argparse
from pathlib import Path

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from backout_source import restore_archive, list_archives

def main():
    parser = argparse.ArgumentParser(
        description="OKF Source & Concept Archive Reincorporator."
    )
    parser.add_argument("bundle_root", nargs="?", default=SCRIPT_DIR.parent, type=Path, help="Bundle directory root")
    parser.add_argument("-a", "--archive", type=str, help="Archive package ID, folder name, or search query to restore")
    parser.add_argument("-l", "--list", action="store_true", help="List all available archives in archive/")

    args = parser.parse_args()
    bundle_dir = args.bundle_root.resolve()

    if args.list:
        list_archives(bundle_dir)
        return

    if not args.archive:
        print("Error: Please specify an archive to restore using --archive <id> or view available archives with --list.")
        sys.exit(1)

    restore_archive(bundle_dir, args.archive)

if __name__ == "__main__":
    main()
