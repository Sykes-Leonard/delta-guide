#!/usr/bin/env python3
"""
compile_graph.py - Extracts and compiles concept documents into viewer/graph-data.json.
Generates an optimized JSON bundle for the DELTA Guide Concept Mind Map SPA.
"""

import re
import json
import sys
from pathlib import Path

# Add scripts directory to path to import parse_yaml_frontmatter
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from validate import parse_yaml_frontmatter

CLUSTER_METADATA = {
    "cluster-human-flourishing": {
        "name": "Human Flourishing",
        "color": "#E5A823",      # Sunlight Gold
        "glow": "#FBD38D",
        "border": "#B7791F",
        "order": 1
    },
    "cluster-moral-agency": {
        "name": "Moral Agency",
        "color": "#3182CE",      # Azure / Indigo
        "glow": "#90CDF4",
        "border": "#2B6CB0",
        "order": 2
    },
    "cluster-power-governance": {
        "name": "Power & Governance",
        "color": "#805AD5",      # Amethyst Violet
        "glow": "#D6BCFA",
        "border": "#6B46C1",
        "order": 3
    },
    "cluster-embodiment-presence": {
        "name": "Embodiment & Presence",
        "color": "#38A169",      # Emerald Forest
        "glow": "#9AE6B4",
        "border": "#2F855A",
        "order": 4
    },
    "cluster-transcendence-truth": {
        "name": "Transcendence & Truth",
        "color": "#DD6B20",      # Sunset Bronze / Delta Ember
        "glow": "#FBD38D",
        "border": "#C05621",
        "order": 5
    }
}

ANCHOR_METADATA = {
    "name": "Central Anchor",
    "color": "#E53E3E",          # Sacred Crimson
    "glow": "#FEB2B2",
    "border": "#9B2C2C",
    "order": 0
}


def extract_section(text: str, heading_pattern: str) -> str:
    """Extracts text under a section heading up until the next ## heading or --- divider."""
    match = re.search(r"##\s+\d*\.?\s*" + heading_pattern + r"\s*\n(.*?)(?=\n##|\n---\s*\n\s*##|\Z)", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""


def clean_markdown_prose(text: str) -> str:
    """Strips markdown links and formatting for clean previews."""
    # Replace [Text](url) with Text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Remove bold/italic markers
    text = text.replace("**", "").replace("*", "")
    return text.strip()


def compile_graph(bundle_dir: Path, output_file: Path) -> dict:
    concepts_dir = bundle_dir / "concepts"
    if not concepts_dir.is_dir():
        print(f"Error: {concepts_dir} does not exist.")
        return {}

    clusters = {}
    concept_to_cluster = {}

    # 1. Parse all cluster documents
    for cf in sorted(concepts_dir.glob("cluster-*.md")):
        slug = cf.stem
        content = cf.read_text(encoding="utf-8")
        meta, body = parse_yaml_frontmatter(content)
        
        info = CLUSTER_METADATA.get(slug, {
            "name": meta.get("title", slug),
            "color": "#CBD5E0",
            "glow": "#E2E8F0",
            "border": "#A0AEC0",
            "order": 99
        })
        
        # Extract constituent concepts
        constituents = []
        links = re.findall(r"\[([^\]]+)\]\(/concepts/([a-zA-Z0-9_\-]+)\.md\)", body)
        for title, cslug in links:
            if not cslug.startswith("cluster-") and cslug not in constituents:
                constituents.append(cslug)
                concept_to_cluster[cslug] = slug
                
        clusters[slug] = {
            "slug": slug,
            "title": meta.get("title", slug),
            "description": meta.get("description", ""),
            "name": info["name"],
            "color": info["color"],
            "glow": info["glow"],
            "border": info["border"],
            "order": info["order"],
            "concepts": constituents,
            "summary": extract_section(body, "Executive Summary")
        }

    # 2. Parse all concept documents
    concepts = {}
    nodes = []
    edges = []
    edge_set = set() # Avoid duplicates: (src, dst, verb)

    for cf in sorted(concepts_dir.glob("*.md")):
        if cf.name.startswith("cluster-") or cf.name == ".gitkeep":
            continue

        slug = cf.stem
        content = cf.read_text(encoding="utf-8")
        meta, body = parse_yaml_frontmatter(content)

        cluster_slug = concept_to_cluster.get(slug)
        if slug == "human-dignity":
            cluster_info = ANCHOR_METADATA
            cluster_name = "Central Anchor"
        elif cluster_slug and cluster_slug in clusters:
            cluster_info = clusters[cluster_slug]
            cluster_name = cluster_info["name"]
        else:
            cluster_info = {
                "color": "#718096",
                "glow": "#CBD5E0",
                "border": "#4A5568"
            }
            cluster_name = "General Concept"

        # Extract structured sections
        exec_summary = extract_section(body, "Executive Summary")
        grounding = extract_section(body, "Theoretical & Institutional Grounding")
        tensions = extract_section(body, "Dialectical Tensions")
        implications = extract_section(body, "Pedagogical, Architectural")

        # Parse Relational Edge Index Table
        edge_index_text = extract_section(body, "Relational Edge Index")
        parsed_edges = []

        # Find rows: | **Outbound** | **[Title](/concepts/target.md)** | *Verb* | Description |
        rows = re.findall(
            r"\|\s*\*{0,2}(Outbound|Inbound)\*{0,2}\s*\|\s*\*{0,2}\[([^\]]+)\]\(/concepts/([a-zA-Z0-9_\-]+)\.md\)\*{0,2}\s*\|\s*\*([^*]+)\*\s*\|\s*([^|\n]+)\|",
            edge_index_text
        )

        for direction, target_title, target_slug, verb, desc in rows:
            clean_verb = verb.strip()
            clean_desc = desc.strip()
            parsed_edges.append({
                "direction": direction.capitalize(),
                "target_slug": target_slug,
                "target_title": target_title.strip(),
                "verb": clean_verb,
                "description": clean_desc
            })

            # Add to global edge graph
            if direction.lower() == "outbound":
                src = slug
                dst = target_slug
            else:
                src = target_slug
                dst = slug

            edge_key = (src, dst, clean_verb)
            if edge_key not in edge_set:
                edge_set.add(edge_key)
                edges.append({
                    "from": src,
                    "to": dst,
                    "label": clean_verb,
                    "verb": clean_verb,
                    "title": f"<b>{clean_verb}</b>: {clean_desc}",
                    "description": clean_desc,
                    "color": {"color": "rgba(229, 168, 35, 0.4)", "highlight": "#F26430", "hover": "#FBD38D"}
                })

        # Add node
        is_anchor = (slug == "human-dignity")
        node_size = 34 if is_anchor else 22

        node_data = {
            "id": slug,
            "slug": slug,
            "label": meta.get("title", slug).split("(")[0].strip(),
            "full_title": meta.get("title", slug),
            "description": meta.get("description", ""),
            "cluster_slug": cluster_slug,
            "cluster_name": cluster_name,
            "is_anchor": is_anchor,
            "tags": meta.get("tags", []),
            "status": meta.get("status", "stable"),
            "sources": meta.get("sources", []),
            "summary": exec_summary,
            "grounding": grounding,
            "tensions": tensions,
            "implications": implications,
            "edges": parsed_edges,
            "color": {
                "background": cluster_info["color"],
                "border": cluster_info["border"],
                "highlight": {
                    "background": cluster_info["glow"],
                    "border": "#FFFFFF"
                },
                "hover": {
                    "background": cluster_info["glow"],
                    "border": cluster_info["color"]
                }
            },
            "font": {
                "color": "#F7F4EE",
                "size": 14 if is_anchor else 12,
                "face": "Inter, system-ui, sans-serif"
            },
            "size": node_size,
            "shadow": {
                "enabled": True,
                "color": cluster_info["color"],
                "size": 18 if is_anchor else 10,
                "x": 0,
                "y": 0
            }
        }

        concepts[slug] = node_data
        nodes.append(node_data)

    compiled_data = {
        "version": "1.0",
        "generated_at": meta.get("generated", {}).get("at", "2026-10-01T21:30:00Z"),
        "clusters": clusters,
        "concepts": concepts,
        "nodes": nodes,
        "edges": edges,
        "stats": {
            "cluster_count": len(clusters),
            "concept_count": len(concepts),
            "edge_count": len(edges)
        }
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(compiled_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Compiled knowledge graph saved to: {output_file}")
    print(f"   • Clusters: {len(clusters)}")
    print(f"   • Concept Nodes: {len(concepts)}")
    print(f"   • Relational Edges: {len(edges)}")
    return compiled_data


if __name__ == "__main__":
    bundle_root = SCRIPT_DIR.parent
    output_path = bundle_root / "viewer" / "graph-data.json"
    compile_graph(bundle_root, output_path)
