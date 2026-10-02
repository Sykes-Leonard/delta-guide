#!/usr/bin/env python3
"""
backout_institution.py - Institutional specialization of backout_source.py.

Safely backs out an external institution and its sources from the knowledge graph.
Delegates directly to the universal backout_source engine.
"""

import sys
from pathlib import Path

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import backout_source

def main():
    # If called without flags or with institution flag, ensure backout_source handles it
    sys.argv[0] = str(Path(__file__).name)
    backout_source.main()

if __name__ == "__main__":
    main()
