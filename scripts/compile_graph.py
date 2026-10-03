#!/usr/bin/env python3
"""
compile_graph.py - Extracts and compiles concept documents into viewer/graph-data.json.
Generates an optimized JSON bundle for the Concept Mind Map & Knowledge Graph visualizer.
"""

import re
import json
import sys
from pathlib import Path

# Add scripts directory to path to import parse_yaml_frontmatter
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from validate import parse_yaml_frontmatter

# Default chromatic palette for clusters if not explicitly declared
DEFAULT_PALETTES = [
    {"color": "#3182CE", "glow": "#90CDF4", "border": "#2B6CB0"},  # Azure
    {"color": "#E5A823", "glow": "#FBD38D", "border": "#B7791F"},  # Sunlight Gold
    {"color": "#805AD5", "glow": "#D6BCFA", "border": "#6B46C1"},  # Amethyst Violet
    {"color": "#38A169", "glow": "#9AE6B4", "border": "#2F855A"},  # Emerald Forest
    {"color": "#DD6B20", "glow": "#FBD38D", "border": "#C05621"},  # Sunset Bronze
    {"color": "#319795", "glow": "#81E6D9", "border": "#285E61"},  # Deep Teal
    {"color": "#D53F8C", "glow": "#FBB6CE", "border": "#97266D"},  # Rose Plum
    {"color": "#4C51BF", "glow": "#A3BFFA", "border": "#3C366B"},  # Royal Indigo
]

ANCHOR_METADATA = {
    "name": "Central Anchor",
    "color": "#E53E3E",          # Crimson
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
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
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
    cluster_idx = 0
    for cf in sorted(concepts_dir.glob("cluster-*.md")):
        slug = cf.stem
        try:
            content = cf.read_text(encoding="utf-8")
        except Exception:
            continue
        meta, body = parse_yaml_frontmatter(content)
        
        palette = DEFAULT_PALETTES[cluster_idx % len(DEFAULT_PALETTES)]
        cluster_idx += 1

        info = {
            "name": meta.get("title", slug).replace("Concept Cluster:", "").strip(),
            "color": meta.get("color", palette["color"]),
            "glow": meta.get("glow", palette["glow"]),
            "border": meta.get("border", palette["border"]),
            "order": cluster_idx
        }
        
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
    edge_set = set()

    for cf in sorted(concepts_dir.glob("*.md")):
        if cf.name.startswith("cluster-") or cf.name == ".gitkeep":
            continue

        slug = cf.stem
        try:
            content = cf.read_text(encoding="utf-8")
        except Exception:
            continue
        meta, body = parse_yaml_frontmatter(content)

        cluster_slug = concept_to_cluster.get(slug)
        is_anchor = meta.get("is_anchor", False) or meta.get("role") == "anchor" or (slug == "human-dignity")

        if is_anchor:
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
        grounding = extract_section(body, "Theoretical.*Grounding")
        tensions = extract_section(body, "Dialectical Tensions")
        implications = extract_section(body, "Applied.*Implications")

        # Parse Relational Edge Index Table
        edge_index_text = extract_section(body, "Relational Edge Index")
        parsed_edges = []

        # Find rows: | (Outbound|Inbound) | [Title](/concepts/target.md) | Verb | Description |
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

        node_size = 32 if is_anchor else 22

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
            "status": meta.get("status", "draft"),
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
        "generated_at": meta.get("generated", {}).get("at", "2026-10-02T00:00:00Z") if 'meta' in locals() else "2026-10-02T00:00:00Z",
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
