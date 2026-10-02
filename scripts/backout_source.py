#!/usr/bin/env python3
"""
backout_source.py - Generalized OKF Source Retraction, Archival & Epistemic Grounding Decoupler.

Audits, retracts, archives, and safely decouples any external source, paper, URL, or institutional container
from the knowledge graph, with full support for safe archival and later reincorporation:
1. Target Resolution: By source ID, resource URL, domain, document, or institutional profile.
2. Grounding Audit: Distinguishes Multi-Grounded concepts from Sole-Grounded (ungrounded) concepts.
3. Graph Blast Radius: Evaluates affected clusters, reciprocal edge indices, Mermaid flowcharts, and links.
4. Archival & Preservation:
   - Stores all backed-out documents and restoration metadata in archive/<archive_id>/.
   - Captures original files, removed frontmatter sources, reciprocal edge rows, and cluster table rows.
5. Flexible Epistemic Actions:
   - prune: Backs out and archives ungrounded concepts, severing reciprocal connections cleanly.
   - draft: Quarantines ungrounded concepts into draft status with warning alerts.
   - substitute: Seamlessly replaces retracted sources with a new peer-reviewed source across all nodes.
6. Reincorporation Engine (--restore):
   - Restores archived files, re-injects frontmatter sources, restores cluster matrix rows and edges.
7. Presubmit Verification: Automatically syncs index.md and runs the presubmit gatekeeper.
"""

import os
import sys
import re
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse

# Add scripts directory to path to reuse validate and update_index
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from validate import parse_yaml_frontmatter, validate_bundle
from update_index import generate_index

# Known domain/prefix mappings for institutions
INSTITUTION_PREFIX_RULES = {
    "deepmind-institute": ["dmi-", "deepmind"],
    "oxford-ethics-ai": ["oxford-", "lyceum"],
    "harvard-human-flourishing": ["harvard-", "vanderweele", "global-flourishing"],
    "council-of-europe-ai": ["coe-", "cets-225"],
    "rome-call-hiroshima": ["rome-", "hiroshima"],
    "un-ai-advisory-body": ["un-", "governing-ai"],
    "berkeley-chai": ["chai-", "berkeley-"],
    "cambridge-cfi": ["cfi-", "cambridge-"],
    "european-ai-office": ["eu-ai-", "gpai-"],
    "stanford-hai": ["stanford-", "crfm-helm"],
    "oecd-ai": ["oecd-"],
    "unesco-ai-ethics": ["unesco-"],
    "russell-group-ai": ["russell-group-"],
    "mit-ai-education": ["mit-ai-", "mit-news-"],
    "cmu-simon-initiative": ["cmu-", "simon-"]
}


def is_institution_domain(host: str, slug: str) -> bool:
    """Returns True if the host is authoritative for the given institution slug."""
    slug_parts = [p for p in slug.split("-") if len(p) > 2 and p not in ["ai", "the", "for", "and", "institute"]]
    for sp in slug_parts:
        if sp in host:
            return True
    if "cambridge" in slug and ("cam.ac.uk" in host or "lcfi" in host):
        return True
    if "oxford" in slug and "ox.ac.uk" in host:
        return True
    if "council-of-europe" in slug and "coe.int" in host:
        return True
    if "rome-call" in slug and "romecall.org" in host:
        return True
    if "deepmind" in slug and "deepmind.com" in host:
        return True
    if "harvard" in slug and "harvard.edu" in host:
        return True
    return False


class UniversalSourceAuditor:
    def __init__(self, bundle_dir: Path):
        self.bundle_dir = bundle_dir
        self.institutions_dir = bundle_dir / "ecosystem" / "institutions"
        self.concepts_dir = bundle_dir / "concepts"
        self.archive_dir = bundle_dir / "archive"
        
        self.all_sources = {}      # sid_or_url -> dict
        self.concepts = {}         # slug -> dict
        self.clusters = {}         # slug -> dict
        self.institutions = {}     # slug -> dict
        self.all_documents = {}    # rel_path -> dict
        self._load_knowledge_graph()

    def _load_knowledge_graph(self):
        for md_path in sorted(self.bundle_dir.glob("**/*.md")):
            if ".git" in str(md_path) or "archive" in md_path.parts or md_path.name.startswith("."):
                continue
            rel_path = md_path.relative_to(self.bundle_dir)
            try:
                content = md_path.read_text(encoding="utf-8")
            except Exception:
                continue

            meta, _ = parse_yaml_frontmatter(content)
            doc_data = {
                "rel_path": str(rel_path),
                "file": md_path,
                "stem": md_path.stem,
                "title": meta.get("title", md_path.stem) if meta else md_path.stem,
                "status": meta.get("status", "draft") if meta else "draft",
                "sources": meta.get("sources", []) if meta else [],
                "content": content
            }
            self.all_documents[str(rel_path)] = doc_data

            # Classify concepts
            if rel_path.parent == Path("concepts"):
                if md_path.name.startswith("cluster-"):
                    self.clusters[md_path.stem] = doc_data
                else:
                    self.concepts[md_path.stem] = doc_data

            # Classify institutions
            if rel_path.parent == Path("ecosystem/institutions") and md_path.stem != "overview":
                self.institutions[md_path.stem] = doc_data

            # Index sources
            for s in doc_data["sources"]:
                if not isinstance(s, dict):
                    continue
                sid = s.get("id") or s.get("resource")
                if not sid:
                    continue
                if sid not in self.all_sources:
                    self.all_sources[sid] = {
                        "id": s.get("id"),
                        "resource": s.get("resource"),
                        "title": s.get("title", ""),
                        "cited_in_concepts": [],
                        "cited_in_other": []
                    }
                if rel_path.parent == Path("concepts") and not md_path.name.startswith("cluster-"):
                    self.all_sources[sid]["cited_in_concepts"].append(md_path.stem)
                else:
                    self.all_sources[sid]["cited_in_other"].append(str(rel_path))

    def resolve_target_sources(
        self,
        source_query: str = None,
        url_query: str = None,
        institution_slug: str = None,
        doc_query: str = None,
        domain_query: str = None
    ) -> tuple[list, dict]:
        """Resolves target parameters into a list of matched sources and context info."""
        target_sources = []
        context = {
            "type": "custom",
            "name": "",
            "container_file": None,
            "is_institution": False
        }

        # Case 1: Institution
        if institution_slug:
            inst = self.institutions.get(institution_slug)
            if not inst:
                matches = [i for s, i in self.institutions.items() if institution_slug in s or institution_slug in i["title"].lower()]
                if len(matches) == 1:
                    inst = matches[0]
                elif len(matches) > 1:
                    raise ValueError(f"Ambiguous institution query '{institution_slug}'. Matches: {[m['stem'] for m in matches]}")
                else:
                    raise ValueError(f"No institution found matching '{institution_slug}'.")

            inst_slug = inst["stem"]
            context["type"] = "institution"
            context["name"] = inst["title"]
            context["container_file"] = inst["file"]
            context["is_institution"] = True
            context["inst_slug"] = inst_slug

            inst_urls = {s.get("resource") for s in inst["sources"] if isinstance(s, dict) and s.get("resource")}
            inst_sids = {s.get("id") for s in inst["sources"] if isinstance(s, dict) and s.get("id")}
            prefixes = INSTITUTION_PREFIX_RULES.get(inst_slug, [inst_slug.split("-")[0]])

            for sid, sdata in self.all_sources.items():
                res = sdata["resource"] or ""
                host = urlparse(res).netloc
                
                is_match = False
                if sid in inst_sids or res in inst_urls:
                    is_match = True
                elif is_institution_domain(host, inst_slug):
                    is_match = True
                elif any(p in sid.lower() for p in prefixes):
                    is_match = True

                if is_match and sdata not in target_sources:
                    target_sources.append(sdata)

        # Case 2: Document
        elif doc_query:
            matched_doc = None
            for rpath, ddata in self.all_documents.items():
                if doc_query in rpath or doc_query == ddata["stem"]:
                    matched_doc = ddata
                    break
            if not matched_doc:
                raise ValueError(f"Document matching '{doc_query}' not found.")

            context["type"] = "document"
            context["name"] = matched_doc["title"]
            context["container_file"] = matched_doc["file"]
            context["doc_rel_path"] = matched_doc["rel_path"]

            doc_urls = {s.get("resource") for s in matched_doc["sources"] if isinstance(s, dict) and s.get("resource")}
            doc_sids = {s.get("id") for s in matched_doc["sources"] if isinstance(s, dict) and s.get("id")}

            for sid, sdata in self.all_sources.items():
                if sid in doc_sids or (sdata["resource"] and sdata["resource"] in doc_urls):
                    target_sources.append(sdata)

        # Case 3: URL
        elif url_query:
            context["type"] = "url"
            context["name"] = url_query
            for sid, sdata in self.all_sources.items():
                if sdata["resource"] and url_query in sdata["resource"]:
                    target_sources.append(sdata)

        # Case 4: Domain
        elif domain_query:
            context["type"] = "domain"
            context["name"] = domain_query
            for sid, sdata in self.all_sources.items():
                res = sdata["resource"] or ""
                if domain_query in urlparse(res).netloc:
                    target_sources.append(sdata)

        # Case 5: Direct Source Query (ID or title)
        elif source_query:
            context["type"] = "source"
            context["name"] = source_query
            for sid, sdata in self.all_sources.items():
                q = source_query.strip().lower()
                if (sdata["id"] and q in sdata["id"].lower()) or \
                   (sdata["resource"] and q in sdata["resource"].lower()) or \
                   (sdata["title"] and q in sdata["title"].lower()):
                    target_sources.append(sdata)

        return target_sources, context

    def audit_retraction(self, target_sources: list, context: dict) -> dict:
        target_ids = {s["id"] for s in target_sources if s.get("id")}
        target_urls = {s["resource"] for s in target_sources if s.get("resource")}

        multi_grounded = []
        sole_grounded = []

        for cslug, cdata in self.concepts.items():
            concept_sources = cdata["sources"]
            matched = []
            surviving = []

            for s in concept_sources:
                if not isinstance(s, dict):
                    continue
                sid = s.get("id")
                res = s.get("resource")
                if (sid and sid in target_ids) or (res and res in target_urls):
                    matched.append(s)
                else:
                    surviving.append(s)

            if matched:
                item = {
                    "slug": cslug,
                    "title": cdata["title"],
                    "file": cdata["file"],
                    "status": cdata["status"],
                    "total_sources_count": len(concept_sources),
                    "matched_sources": matched,
                    "surviving_sources": surviving
                }
                if len(surviving) == 0:
                    sole_grounded.append(item)
                else:
                    multi_grounded.append(item)

        # Blast radius analysis for sole-grounded concepts
        graph_blast_radius = {}
        for s_item in sole_grounded:
            cslug = s_item["slug"]
            blast = {
                "clusters": [],
                "cluster_rows": {},
                "reciprocal_edges": {},
                "mermaid_references": [],
                "inbound_links": []
            }
            # Check cluster memberships and capture exact table rows
            for cl_slug, cl_data in self.clusters.items():
                link_pattern = f"/concepts/{cslug}.md"
                if link_pattern in cl_data["content"] or f"/concepts/{cslug}" in cl_data["content"]:
                    blast["clusters"].append(cl_slug)
                    for line in cl_data["content"].splitlines():
                        if line.strip().startswith("|") and link_pattern in line:
                            blast["cluster_rows"][cl_slug] = line

            # Check other concepts
            for peer_slug, peer_data in self.concepts.items():
                if peer_slug == cslug:
                    continue
                content = peer_data["content"]
                link_pattern = f"/concepts/{cslug}.md"
                if link_pattern in content:
                    blast["inbound_links"].append(peer_slug)
                if link_pattern in content and "## 6. Relational Edge Index" in content:
                    edge_rows = []
                    for line in content.splitlines():
                        if line.strip().startswith("|") and link_pattern in line:
                            edge_rows.append(line)
                    if edge_rows:
                        blast["reciprocal_edges"][peer_slug] = edge_rows

                if "```mermaid" in content:
                    m_blocks = re.findall(r"```mermaid(.*?)```", content, re.DOTALL)
                    for mb in m_blocks:
                        if s_item["title"].split()[0].lower() in mb.lower() or cslug.split("-")[0].lower() in mb.lower():
                            blast["mermaid_references"].append(peer_slug)

            graph_blast_radius[cslug] = blast

        # Check references to container document if applicable
        container_inbound_links = []
        overview_row = None
        if context.get("container_file"):
            container_rel = context["container_file"].relative_to(self.bundle_dir)
            target_link = f"/{container_rel}"
            for rpath, ddata in self.all_documents.items():
                if ddata["file"] != context["container_file"] and target_link in ddata["content"]:
                    container_inbound_links.append(rpath)
                    
            if context.get("is_institution"):
                overview_path = self.institutions_dir / "overview.md"
                if overview_path.is_file():
                    inst_link = f"/ecosystem/institutions/{context['inst_slug']}.md"
                    for line in overview_path.read_text(encoding="utf-8").splitlines():
                        if line.strip().startswith("|") and inst_link in line:
                            overview_row = line
                            break

        return {
            "context": context,
            "target_sources": target_sources,
            "multi_grounded": multi_grounded,
            "sole_grounded": sole_grounded,
            "graph_blast_radius": graph_blast_radius,
            "container_inbound_links": container_inbound_links,
            "overview_row": overview_row
        }


def format_audit_report(result: dict) -> str:
    ctx = result["context"]
    targets = result["target_sources"]
    multi = result["multi_grounded"]
    sole = result["sole_grounded"]
    blast = result["graph_blast_radius"]
    container_links = result["container_inbound_links"]

    lines = []
    lines.append(f"════════════════════════════════════════════════════════════════════════════════")
    lines.append(f" 📑 SOURCE RETRACTION AUDIT: [{ctx['type'].upper()}] {ctx['name']}")
    if ctx.get("container_file"):
        lines.append(f"    Container File: {ctx['container_file'].relative_to(Path.cwd())}")
    lines.append(f"════════════════════════════════════════════════════════════════════════════════\n")

    lines.append(f"📦 Target Sources to Retract ({len(targets)}):")
    for s in targets:
        lines.append(f"   • [{s.get('id')}] {s.get('title')} ({s.get('resource')})")
    lines.append("")

    lines.append(f"📊 Concept Epistemic Grounding Impact:")
    lines.append(f"   • Multi-Grounded Concepts (Survives: ≥ 1 source remaining): {len(multi)}")
    lines.append(f"   • Sole-Grounded Concepts (Critically Depleted: 0 sources remaining): {len(sole)}")
    lines.append("")

    if multi:
        lines.append("────────────────────────────────────────────────────────────────────────────────")
        lines.append(f"🟢 MULTI-GROUNDED CONCEPTS ({len(multi)} nodes survive with independent sources):")
        lines.append("────────────────────────────────────────────────────────────────────────────────")
        for m in multi:
            lines.append(f"   ✔ concepts/{m['slug']}.md")
            lines.append(f"     Title: {m['title']}")
            lines.append(f"     Retracted Sources: {[s.get('id') for s in m['matched_sources']]}")
            lines.append(f"     Surviving Sources ({len(m['surviving_sources'])}): {[s.get('id') for s in m['surviving_sources']]}")
            lines.append("")

    if sole:
        lines.append("────────────────────────────────────────────────────────────────────────────────")
        lines.append(f"🚨 SOLE-GROUNDED CONCEPTS ({len(sole)} nodes lose ALL source grounding):")
        lines.append("────────────────────────────────────────────────────────────────────────────────")
        for s in sole:
            lines.append(f"   ❌ concepts/{s['slug']}.md")
            lines.append(f"      Title: {s['title']}")
            lines.append(f"      Retracted Sources: {[src.get('id') for src in s['matched_sources']]}")
            lines.append(f"      Remaining Sources: 0 (Ungrounded!)")
            
            b = blast.get(s["slug"], {})
            if b.get("clusters"):
                lines.append(f"      Parent Cluster(s): {', '.join(b['clusters'])}")
            if b.get("reciprocal_edges"):
                lines.append(f"      Reciprocal Edge Tables to Prune: {', '.join(b['reciprocal_edges'].keys())}")
            if b.get("mermaid_references"):
                lines.append(f"      Mermaid Flowcharts to Prune: {', '.join(b['mermaid_references'])}")
            if b.get("inbound_links"):
                lines.append(f"      Inbound Markdown References: {len(b['inbound_links'])} file(s)")
            lines.append("")
    else:
        lines.append("✨ No concepts are sole-grounded. Zero concepts will be ungrounded.\n")

    if container_links:
        lines.append("────────────────────────────────────────────────────────────────────────────────")
        lines.append(f"🔗 INBOUND REFERENCES TO SOURCE CONTAINER FILE ({len(container_links)} files):")
        lines.append("────────────────────────────────────────────────────────────────────────────────")
        for cl in container_links[:10]:
            lines.append(f"   • {cl}")
        if len(container_links) > 10:
            lines.append(f"   ... and {len(container_links) - 10} more files.")
        lines.append("")

    return "\n".join(lines)


def remove_sources_from_frontmatter(content: str, ids_or_urls_to_remove: set) -> str:
    parts = content.split("---", 2)
    if len(parts) < 3:
        return content
    fm = parts[1]
    body = parts[2]
    
    lines = fm.splitlines()
    new_lines = []
    in_sources = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"^sources\s*:", line):
            in_sources = True
            new_lines.append(line)
            i += 1
            continue
            
        if in_sources:
            if re.match(r"^[a-zA-Z0-9_\-]+:", line):
                in_sources = False
                new_lines.append(line)
                i += 1
                continue
            if line.startswith("  - "):
                item_lines = [line]
                j = i + 1
                while j < len(lines) and (lines[j].startswith("    ") or lines[j].startswith("      ")):
                    item_lines.append(lines[j])
                    j += 1
                item_block = "\n".join(item_lines)
                should_remove = any(target in item_block for target in ids_or_urls_to_remove)
                if not should_remove:
                    new_lines.extend(item_lines)
                i = j
                continue
            elif line.strip() == "":
                new_lines.append(line)
                i += 1
                continue
        new_lines.append(line)
        i += 1
        
    new_fm = "\n".join(new_lines)
    if not new_fm.endswith("\n"):
        new_fm += "\n"
    return "---" + new_fm + "---" + body


def add_sources_to_frontmatter(content: str, sources_to_add: list) -> str:
    parts = content.split("---", 2)
    if len(parts) < 3:
        return content
    fm = parts[1]
    body = parts[2]
    
    lines = fm.splitlines()
    sources_idx = -1
    for idx, l in enumerate(lines):
        if re.match(r"^sources\s*:", l):
            sources_idx = idx
            break
            
    source_lines = []
    for s in sources_to_add:
        source_lines.append(f"  - id: {s.get('id', '')}")
        source_lines.append(f"    resource: {s.get('resource', '')}")
        s_title = s.get("title", "")
        source_lines.append(f'    title: "{s_title}"')
        
    if sources_idx != -1:
        new_lines = lines[:sources_idx+1] + source_lines + lines[sources_idx+1:]
    else:
        new_lines = lines + ["sources:"] + source_lines
        
    new_fm = "\n".join(new_lines)
    if not new_fm.endswith("\n"):
        new_fm += "\n"
    return "---" + new_fm + "---" + body


def substitute_source_in_frontmatter(content: str, old_targets: set, new_id: str, new_url: str, new_title: str) -> str:
    parts = content.split("---", 2)
    if len(parts) < 3:
        return content
    fm = parts[1]
    body = parts[2]
    
    lines = fm.splitlines()
    new_lines = []
    in_sources = False
    substituted = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"^sources\s*:", line):
            in_sources = True
            new_lines.append(line)
            i += 1
            continue
            
        if in_sources:
            if re.match(r"^[a-zA-Z0-9_\-]+:", line):
                in_sources = False
                new_lines.append(line)
                i += 1
                continue
            if line.startswith("  - "):
                item_lines = [line]
                j = i + 1
                while j < len(lines) and (lines[j].startswith("    ") or lines[j].startswith("      ")):
                    item_lines.append(lines[j])
                    j += 1
                item_block = "\n".join(item_lines)
                is_match = any(target in item_block for target in old_targets)
                if is_match and not substituted:
                    new_lines.append(f"  - id: {new_id}")
                    new_lines.append(f"    resource: {new_url}")
                    new_lines.append(f'    title: "{new_title}"')
                    substituted = True
                elif not is_match:
                    new_lines.extend(item_lines)
                i = j
                continue
            elif line.strip() == "":
                new_lines.append(line)
                i += 1
                continue
        new_lines.append(line)
        i += 1
        
    new_fm = "\n".join(new_lines)
    if not new_fm.endswith("\n"):
        new_fm += "\n"
    return "---" + new_fm + "---" + body


def clean_mermaid_node(content: str, concept_title: str, concept_slug: str) -> str:
    parts = re.split(r"(```mermaid.*?```)", content, flags=re.DOTALL)
    if len(parts) < 2:
        return content

    words = [w for w in re.split(r"[^a-zA-Z0-9]+", concept_title) if len(w) > 3]
    if not words:
        words = [concept_slug.split("-")[0]]

    def clean_block(mermaid_block: str) -> str:
        key = None
        for w in words:
            m = re.search(rf"([A-Z0-9_]+)\[[^\]]*{re.escape(w)}", mermaid_block, re.IGNORECASE)
            if m:
                key = m.group(1)
                break
        if not key:
            return mermaid_block

        lines = mermaid_block.splitlines()
        new_lines = []
        skip_multiline = False
        for line in lines:
            if skip_multiline:
                if '"]' in line or "]" in line:
                    skip_multiline = False
                continue
            if re.search(rf"^\s*{key}\[", line):
                if not ('"]' in line or "]" in line):
                    skip_multiline = True
                continue
            if key in line and any(arrow in line for arrow in ["-->", "-.->", "==>", "---"]):
                continue
            new_lines.append(line)
        return "\n".join(new_lines)

    for idx, part in enumerate(parts):
        if part.startswith("```mermaid"):
            parts[idx] = clean_block(part)

    return "".join(parts)


def clean_reciprocal_edges_and_links(content: str, target_slug: str, target_title: str) -> str:
    content = clean_mermaid_node(content, target_title, target_slug)

    lines = content.splitlines()
    new_lines = []
    link_pattern = f"/concepts/{target_slug}.md"
    for line in lines:
        if line.strip().startswith("|") and link_pattern in line:
            continue
        new_lines.append(line)
    content = "\n".join(new_lines)

    content = re.sub(rf"^\s*\*\s+\[.*?\]\(/concepts/{re.escape(target_slug)}\.md\).*?\n", "", content, flags=re.MULTILINE)
    content = re.sub(rf"\[([^\]]+)\]\(/concepts/{re.escape(target_slug)}\.md\)", r"**\1**", content)
    return content


def remove_from_cluster_file(cluster_path: Path, target_slug: str, target_title: str):
    if not cluster_path.is_file():
        return
    content = cluster_path.read_text(encoding="utf-8")
    content = clean_mermaid_node(content, target_title, target_slug)

    lines = content.splitlines()
    new_lines = []
    link_pattern = f"/concepts/{target_slug}.md"
    for line in lines:
        if line.strip().startswith("|") and link_pattern in line:
            continue
        new_lines.append(line)
    content = "\n".join(new_lines)

    content = re.sub(rf"\[([^\]]+)\]\(/concepts/{re.escape(target_slug)}\.md\)", r"**\1**", content)
    cluster_path.write_text(content, encoding="utf-8")


def reinsert_table_row(text: str, header: str, row_str: str) -> str:
    """Inserts a Markdown table row into a specific section table if not already present."""
    if row_str in text:
        return text
    if header in text:
        parts = text.split(header, 1)
        sub = parts[1]
        lines = sub.splitlines()
        last_table_line = -1
        for idx, l in enumerate(lines):
            if l.strip().startswith("|") and ("---" in l or ":---" in l):
                continue
            if l.strip().startswith("|"):
                last_table_line = idx
        if last_table_line != -1:
            lines.insert(last_table_line + 1, row_str)
            return parts[0] + header + "\n" + "\n".join(lines)
    return text


def remove_from_overview_file(overview_path: Path, inst_slug: str):
    if not overview_path.is_file():
        return
    content = overview_path.read_text(encoding="utf-8")
    link_pattern = f"/ecosystem/institutions/{inst_slug}.md"

    lines = content.splitlines()
    new_lines = []
    for line in lines:
        if line.strip().startswith("|") and link_pattern in line:
            continue
        new_lines.append(line)
    content = "\n".join(new_lines)
    overview_path.write_text(content, encoding="utf-8")


def replace_document_links_repo(bundle_dir: Path, target_rel_path: str):
    target_link = f"/{target_rel_path}"
    for p in bundle_dir.glob("**/*.md"):
        if ".git" in str(p) or "archive" in p.parts:
            continue
        try:
            txt = p.read_text(encoding="utf-8")
            if target_link in txt:
                new_txt = re.sub(rf"\[([^\]]+)\]\({re.escape(target_link)}\)", r"**\1**", txt)
                if new_txt != txt:
                    p.write_text(new_txt, encoding="utf-8")
        except Exception:
            pass


def create_archive_package(
    bundle_dir: Path,
    audit_result: dict,
    action_ungrounded: str,
    delete_container_doc: bool
) -> Path:
    """Packages all backed-out documents and restoration metadata into archive/<archive_id>/."""
    ctx = audit_result["context"]
    targets = audit_result["target_sources"]
    multi = audit_result["multi_grounded"]
    sole = audit_result["sole_grounded"]
    blast = audit_result["graph_blast_radius"]

    now = datetime.now(timezone.utc)
    timestamp_str = now.strftime("%Y-%m-%d_%H%M%S")
    clean_name = re.sub(r"[^a-zA-Z0-9_\-]+", "-", ctx["name"].lower()).strip("-")[:40]
    archive_id = f"{timestamp_str}_{clean_name}"
    
    archive_path = bundle_dir / "archive" / archive_id
    files_dir = archive_path / "files"
    files_dir.mkdir(parents=True, exist_ok=True)

    backed_out_files = []

    # 1. Archive container document if slated for deletion
    if delete_container_doc and ctx.get("container_file") and ctx["container_file"].is_file():
        cfile = ctx["container_file"]
        rel = cfile.relative_to(bundle_dir)
        dest = files_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(cfile, dest)
        backed_out_files.append(str(rel))

    # 2. Archive pruned concept files
    if action_ungrounded == "prune":
        for s in sole:
            cfile = s["file"]
            if cfile.is_file():
                rel = cfile.relative_to(bundle_dir)
                dest = files_dir / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(cfile, dest)
                backed_out_files.append(str(rel))

    # 3. Build manifest metadata
    multi_grounded_updates = {}
    for m in multi:
        rel = str(m["file"].relative_to(bundle_dir))
        multi_grounded_updates[rel] = m["matched_sources"]

    manifest = {
        "okf_archive_version": "1.0",
        "archive_id": archive_id,
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "target_type": ctx["type"],
        "target_name": ctx["name"],
        "is_institution": ctx.get("is_institution", False),
        "inst_slug": ctx.get("inst_slug"),
        "action_ungrounded": action_ungrounded,
        "status": "archived",
        "retracted_sources": targets,
        "backed_out_files": backed_out_files,
        "multi_grounded_updates": multi_grounded_updates,
        "pruned_concepts_info": {
            s["slug"]: {
                "title": s["title"],
                "parent_clusters": blast.get(s["slug"], {}).get("clusters", []),
                "cluster_rows": blast.get(s["slug"], {}).get("cluster_rows", {}),
                "reciprocal_edges": blast.get(s["slug"], {}).get("reciprocal_edges", {})
            }
            for s in sole
        },
        "overview_row": audit_result.get("overview_row")
    }

    manifest_path = archive_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    
    return archive_path


def restore_archive(bundle_dir: Path, archive_query: str):
    """Restores an archive package back into the active knowledge graph."""
    archive_dir = bundle_dir / "archive"
    target_archive = None

    if (archive_dir / archive_query).is_dir():
        target_archive = archive_dir / archive_query
    else:
        # Fuzzy match
        for d in sorted(archive_dir.glob("*")):
            if d.is_dir() and (archive_query in d.name):
                target_archive = d
                break

    if not target_archive or not (target_archive / "manifest.json").is_file():
        print(f"Error: Archive '{archive_query}' not found in {archive_dir}.")
        sys.exit(1)

    manifest = json.loads((target_archive / "manifest.json").read_text(encoding="utf-8"))
    archive_id = manifest["archive_id"]
    files_dir = target_archive / "files"

    print(f"\n🔄 REINCORPORATING ARCHIVE: {archive_id}")
    print(f"   Target: [{manifest['target_type'].upper()}] {manifest['target_name']}")
    print(f"   Archived on: {manifest['timestamp']}\n")

    # 1. Restore files
    if files_dir.is_dir():
        for f in files_dir.glob("**/*"):
            if f.is_file():
                rel = f.relative_to(files_dir)
                dest = bundle_dir / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
                print(f"  ✔ Restored file: {rel}")

    # 2. Restore multi-grounded sources in surviving concepts
    for rel_path, restored_sources in manifest.get("multi_grounded_updates", {}).items():
        doc_path = bundle_dir / rel_path
        if doc_path.is_file():
            content = doc_path.read_text(encoding="utf-8")
            new_content = add_sources_to_frontmatter(content, restored_sources)
            doc_path.write_text(new_content, encoding="utf-8")
            print(f"  ✔ Restored source citations: {rel_path}")

    # 3. Restore cluster table rows and reciprocal edges for pruned concepts
    pruned_info = manifest.get("pruned_concepts_info", {})
    for cslug, pdata in pruned_info.items():
        ctitle = pdata.get("title", cslug)
        
        # Restore cluster matrix rows
        for cl_slug, row_str in pdata.get("cluster_rows", {}).items():
            cl_path = bundle_dir / "concepts" / f"{cl_slug}.md"
            if cl_path.is_file():
                txt = cl_path.read_text(encoding="utf-8")
                new_txt = reinsert_table_row(txt, "## 3. Constituent Concepts Matrix", row_str)
                if new_txt != txt:
                    cl_path.write_text(new_txt, encoding="utf-8")
                    print(f"  ✔ Restored cluster row in concepts/{cl_slug}.md")

        # Restore reciprocal edge rows in peer concepts
        for peer_slug, edge_rows in pdata.get("reciprocal_edges", {}).items():
            peer_path = bundle_dir / "concepts" / f"{peer_slug}.md"
            if peer_path.is_file():
                txt = peer_path.read_text(encoding="utf-8")
                for row_str in edge_rows:
                    txt = reinsert_table_row(txt, "## 6. Relational Edge Index", row_str)
                peer_path.write_text(txt, encoding="utf-8")
                print(f"  ✔ Restored reciprocal edges in concepts/{peer_slug}.md")

    # 4. Restore overview row if institution
    if manifest.get("is_institution") and manifest.get("overview_row"):
        overview_path = bundle_dir / "ecosystem" / "institutions" / "overview.md"
        if overview_path.is_file():
            txt = overview_path.read_text(encoding="utf-8")
            new_txt = reinsert_table_row(txt, "## 2. Institutional Landscape Matrix", manifest["overview_row"])
            if new_txt != txt:
                overview_path.write_text(new_txt, encoding="utf-8")
                print(f"  ✔ Restored registry matrix row in ecosystem/institutions/overview.md")

    # 5. Mark manifest as reincorporated
    manifest["status"] = "reincorporated"
    manifest["reincorporated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    (target_archive / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # 6. Append to log.md
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log_entry = [
        f"## {today_str}",
        f"* **Reincorporation**: Restored and reincorporated [{manifest['target_name']}] from archive package `{archive_id}`.",
        f"  - Restored {len(manifest.get('backed_out_files', []))} files, concept groundings, and relational graph edges.\n"
    ]
    log_path = bundle_dir / "log.md"
    if log_path.is_file():
        old = log_path.read_text(encoding="utf-8")
        if f"## {today_str}" in old:
            parts = old.split(f"## {today_str}\n", 1)
            new_log = parts[0] + f"## {today_str}\n" + "\n".join(log_entry[1:]) + "\n" + parts[1]
        else:
            new_log = f"# {old.splitlines()[0][2:]}\n\n" + "\n".join(log_entry) + "\n" + "\n".join(old.splitlines()[2:])
        log_path.write_text(new_log, encoding="utf-8")
        print(f"  ✔ Appended reincorporation audit entry to log.md")

    # 7. Resync index.md
    print("\n🔄 Synchronizing index.md...")
    generate_index(bundle_dir)

    # 8. Presubmit Validation
    print("\n🛡️  Running OKF Presubmit Gatekeeper (Zero-Defect Verification)...")
    res = validate_bundle(bundle_dir, fix=True)
    if res == 0:
        print(f"\n✅ Reincorporation of '{archive_id}' succeeded with ZERO errors and ZERO warnings!\n")
    else:
        print(f"\n⚠️  Presubmit finished with exit code {res}. Please check remaining warnings.\n")


def append_to_log(
    bundle_dir: Path,
    source_desc: str,
    archive_id: str,
    pruned_concepts: list,
    drafted_concepts: list,
    substituted_concepts: list,
    multi_concepts: list
):
    log_path = bundle_dir / "log.md"
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    entry_lines = [
        f"## {today_str}",
        f"* **Source Retraction & Archival**: Retracted [{source_desc}] and preserved in archive (`{archive_id}`).",
    ]
    if pruned_concepts:
        entry_lines.append(f"  - **Archived & Pruned Concepts**: {', '.join(f'`{c}`' for c in pruned_concepts)} (depleted ground truth).")
    if drafted_concepts:
        entry_lines.append(f"  - **Quarantined to Draft**: {', '.join(f'`{c}`' for c in drafted_concepts)} pending re-grounding.")
    if substituted_concepts:
        entry_lines.append(f"  - **Re-Grounded Concepts**: Substituted alternative primary source for {len(substituted_concepts)} concept node(s).")
    if multi_concepts:
        entry_lines.append(f"  - **Updated Source Provenance**: Removed retracted citation from {len(multi_concepts)} resilient concept node(s).")
    entry_lines.append("")

    new_entry = "\n".join(entry_lines) + "\n"

    if log_path.is_file():
        old_content = log_path.read_text(encoding="utf-8")
        if f"## {today_str}" in old_content:
            parts = old_content.split(f"## {today_str}\n", 1)
            updated_content = parts[0] + f"## {today_str}\n" + "\n".join(entry_lines[1:]) + "\n" + parts[1]
        else:
            lines = old_content.splitlines()
            insert_idx = 0
            for idx, l in enumerate(lines):
                if l.startswith("# "):
                    insert_idx = idx + 2
                    break
            updated_content = "\n".join(lines[:insert_idx]) + "\n\n" + new_entry + "\n".join(lines[insert_idx:])
        log_path.write_text(updated_content, encoding="utf-8")


def apply_retraction(
    bundle_dir: Path,
    audit_result: dict,
    action_ungrounded: str = "prune",
    delete_container_doc: bool = False,
    substitute_id: str = None,
    substitute_url: str = None,
    substitute_title: str = None
):
    ctx = audit_result["context"]
    targets = audit_result["target_sources"]
    multi = audit_result["multi_grounded"]
    sole = audit_result["sole_grounded"]
    
    retracted_targets = set()
    for s in targets:
        if s.get("id"):
            retracted_targets.add(s["id"])
        if s.get("resource"):
            retracted_targets.add(s["resource"])

    print(f"\n🚀 Applying Source Retraction for: {ctx['name']} ({len(targets)} sources)...\n")

    # STEP 0: Create Archive Package FIRST before any mutations!
    archive_path = create_archive_package(
        bundle_dir,
        audit_result,
        action_ungrounded,
        delete_container_doc
    )
    archive_id = archive_path.name
    print(f"  📦 Archived backed-out assets and restoration manifest to:\n     archive/{archive_id}/\n")

    multi_slugs = []
    # 1. Multi-Grounded Concepts: strip retracted sources from frontmatter
    for m in multi:
        cfile = m["file"]
        content = cfile.read_text(encoding="utf-8")
        new_content = remove_sources_from_frontmatter(content, retracted_targets)
        cfile.write_text(new_content, encoding="utf-8")
        multi_slugs.append(m["slug"])
        print(f"  ✔ Updated frontmatter sources: concepts/{m['slug']}.md")

    pruned_slugs = []
    drafted_slugs = []
    substituted_slugs = []

    # 2. Sole-Grounded Concepts: handle action
    for s in sole:
        cslug = s["slug"]
        cfile = s["file"]
        ctitle = s["title"]

        action = action_ungrounded
        if action == "prompt":
            resp = input(f"Choose action for sole-grounded concept '{ctitle}' [p]rune, [d]raft, [s]ubstitute: ").strip().lower()
            if resp.startswith("s"):
                action = "substitute"
            elif resp.startswith("d"):
                action = "draft"
            else:
                action = "prune"

        if action == "substitute":
            sub_id = substitute_id or f"source:{cslug}-regrounded"
            sub_url = substitute_url or "https://arxiv.org/"
            sub_title = substitute_title or f"Primary Grounding for {ctitle}"
            
            content = cfile.read_text(encoding="utf-8")
            new_content = substitute_source_in_frontmatter(content, retracted_targets, sub_id, sub_url, sub_title)
            cfile.write_text(new_content, encoding="utf-8")
            substituted_slugs.append(cslug)
            print(f"  ✔ Re-grounded concept with substitute source: concepts/{cslug}.md -> [{sub_id}]")

        elif action == "draft":
            content = cfile.read_text(encoding="utf-8")
            content = re.sub(r"^status:\s*stable", "status: draft", content, flags=re.MULTILINE)
            content = remove_sources_from_frontmatter(content, retracted_targets)
            alert = "\n> [!WARNING] Grounding Depleted\n> This concept's primary grounding was retracted. Preserved in draft status pending re-grounding.\n\n"
            content = re.sub(r"(#\s+[^\n]+\n)", r"\1" + alert, content, count=1)
            cfile.write_text(content, encoding="utf-8")
            drafted_slugs.append(cslug)
            print(f"  ✔ Quarantined ungrounded concept to draft: concepts/{cslug}.md")

        elif action == "prune":
            if cfile.is_file():
                cfile.unlink()
            pruned_slugs.append(cslug)
            print(f"  ✔ Deleted concept file: concepts/{cslug}.md")

            # Remove from parent clusters
            for cl_file in (bundle_dir / "concepts").glob("cluster-*.md"):
                remove_from_cluster_file(cl_file, cslug, ctitle)

            # Sever reciprocal edges in other concepts
            for other_cfile in (bundle_dir / "concepts").glob("*.md"):
                if other_cfile.name.startswith("cluster-"):
                    continue
                try:
                    c_txt = other_cfile.read_text(encoding="utf-8")
                    if f"/concepts/{cslug}.md" in c_txt:
                        new_c_txt = clean_reciprocal_edges_and_links(c_txt, cslug, ctitle)
                        if new_c_txt != c_txt:
                            other_cfile.write_text(new_c_txt, encoding="utf-8")
                            print(f"    - Cleaned reciprocal edges in concepts/{other_cfile.name}")
                except Exception:
                    pass

            # Clean references in systems/ playbooks/ ecosystem/
            for folder in ["systems", "ecosystem", "playbooks", "research"]:
                f_dir = bundle_dir / folder
                if f_dir.is_dir():
                    for doc in f_dir.glob("**/*.md"):
                        try:
                            d_txt = doc.read_text(encoding="utf-8")
                            if f"/concepts/{cslug}.md" in d_txt:
                                new_d_txt = re.sub(rf"\[([^\]]+)\]\(/concepts/{re.escape(cslug)}\.md\)", r"**\1**", d_txt)
                                doc.write_text(new_d_txt, encoding="utf-8")
                        except Exception:
                            pass

    # 3. Clean up container document if requested
    if delete_container_doc and ctx.get("container_file") and ctx["container_file"].is_file():
        cfile = ctx["container_file"]
        rel_path = str(cfile.relative_to(bundle_dir))
        cfile.unlink()
        print(f"  ✔ Deleted source container file: {rel_path}")

        if ctx.get("is_institution"):
            overview_file = bundle_dir / "ecosystem" / "institutions" / "overview.md"
            remove_from_overview_file(overview_file, ctx["inst_slug"])
            print(f"  ✔ Removed from registry matrix: ecosystem/institutions/overview.md")

        replace_document_links_repo(bundle_dir, rel_path)
        print(f"  ✔ Normalized inbound markdown links to container document across workspace.")

    # 4. Append to log.md
    append_to_log(bundle_dir, ctx["name"], archive_id, pruned_slugs, drafted_slugs, substituted_slugs, multi_slugs)
    print(f"  ✔ Appended audit entry to log.md")

    # 5. Synchronize index.md
    print("\n🔄 Synchronizing index.md...")
    generate_index(bundle_dir)

    # 6. Run Presubmit Validation
    print("\n🛡️  Running OKF Presubmit Gatekeeper (Zero-Defect Verification)...")
    res = validate_bundle(bundle_dir, fix=True)
    if res == 0:
        print(f"\n✅ Source retraction completed cleanly with ZERO errors and ZERO warnings!")
        print(f"📦 Archive preserved at: archive/{archive_id}/")
        print(f"💡 To reincorporate or restore this asset later, run:")
        print(f"   python3 scripts/backout_source.py --restore {archive_id}\n")
    else:
        print(f"\n⚠️  Presubmit finished with exit code {res}. Please check remaining warnings.\n")


def list_archives(bundle_dir: Path):
    archive_dir = bundle_dir / "archive"
    if not archive_dir.is_dir():
        print("No archives found (archive/ directory does not exist).")
        return

    archives = []
    for d in sorted(archive_dir.glob("*"), reverse=True):
        if d.is_dir() and (d / "manifest.json").is_file():
            try:
                m = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
                archives.append((d.name, m))
            except Exception:
                pass

    if not archives:
        print("No archives found in archive/.")
        return

    print(f"\n{'Archive ID':<35} {'Status':<15} {'Type':<12} {'Target Name'}")
    print("─" * 90)
    for aid, m in archives:
        status_str = "🟢 Restored" if m.get("status") == "reincorporated" else "📦 Archived"
        print(f"{aid:<35} {status_str:<15} {m.get('target_type', ''):<12} {m.get('target_name', '')}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="OKF Knowledge Base Universal Source Retraction, Archival & Epistemic Grounding Decoupler."
    )
    parser.add_argument("bundle_root", nargs="?", default=SCRIPT_DIR.parent, type=Path, help="Bundle directory root")
    
    # Target selectors
    parser.add_argument("-s", "--source", type=str, help="Source ID, title, or search query to retract")
    parser.add_argument("-u", "--url", type=str, help="Exact or partial source URL to retract")
    parser.add_argument("-i", "--institution", type=str, help="Institution slug whose sources should be retracted")
    parser.add_argument("-d", "--doc", type=str, help="Document path or stem whose sources should be retracted")
    parser.add_argument("--domain", type=str, help="Domain whose sources should be retracted (e.g. arxiv.org, deepmind.com)")
    
    # Discovery listings
    parser.add_argument("--list", action="store_true", help="List all sources across the knowledge base with citation counts")
    parser.add_argument("--list-institutions", action="store_true", help="List institutions with their source counts")
    parser.add_argument("--list-archives", action="store_true", help="List all archived source/institution packages in archive/")

    # Reincorporation / Restore
    parser.add_argument("--restore", type=str, help="Restore an archive package back into the active knowledge graph")

    # Execution controls
    parser.add_argument("--dry-run", action="store_true", default=True, help="Perform dry-run analysis without making changes (default)")
    parser.add_argument("--apply", action="store_true", help="Execute the retraction, archival, and edge pruning")
    parser.add_argument(
        "--action-ungrounded",
        choices=["prune", "draft", "substitute", "prompt"],
        default="prune",
        help="Action for concepts that lose 100%% of sources: 'prune', 'draft', 'substitute', or 'prompt'"
    )
    
    # Substitution parameters
    parser.add_argument("--substitute-id", type=str, help="Replacement source ID for --action-ungrounded substitute")
    parser.add_argument("--substitute-url", type=str, help="Replacement source URL for --action-ungrounded substitute")
    parser.add_argument("--substitute-title", type=str, help="Replacement source title for --action-ungrounded substitute")
    
    # Container document cleanup
    parser.add_argument("--delete-doc", action="store_true", help="Also delete the source-defining document (e.g. institution profile)")

    args = parser.parse_args()
    bundle_dir = args.bundle_root.resolve()

    # Restore mode
    if args.restore:
        restore_archive(bundle_dir, args.restore)
        return

    # List archives mode
    if args.list_archives:
        list_archives(bundle_dir)
        return

    auditor = UniversalSourceAuditor(bundle_dir)

    # List modes
    if args.list:
        print(f"\n{'Source ID':<38} {'Cited in Concepts':<20} {'Resource URL'}")
        print("─" * 90)
        for sid, sdata in sorted(auditor.all_sources.items(), key=lambda x: len(x[1]['cited_in_concepts']), reverse=True):
            res_str = sdata['resource'] or ''
            if len(res_str) > 40:
                res_str = res_str[:37] + "..."
            c_count = len(sdata['cited_in_concepts'])
            print(f"{sid:<38} {c_count:<20} {res_str}")
        print(f"\nTotal unique sources: {len(auditor.all_sources)}\n")
        return

    if args.list_institutions:
        print(f"\n{'Institution Slug':<30} {'Sources':<10} {'Title'}")
        print("─" * 80)
        for slug, data in auditor.institutions.items():
            print(f"{slug:<30} {len(data['sources']):<10} {data['title']}")
        print()
        return

    # Check that a target was specified
    if not (args.source or args.url or args.institution or args.doc or args.domain):
        print("Error: Please specify a target using --source, --url, --institution, --doc, or --domain.")
        print("Use --list to inspect all available sources, --list-institutions to view institutions, or --list-archives to view archives.")
        sys.exit(1)

    try:
        targets, ctx = auditor.resolve_target_sources(
            source_query=args.source,
            url_query=args.url,
            institution_slug=args.institution,
            doc_query=args.doc,
            domain_query=args.domain
        )
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if not targets:
        print(f"No sources matched the criteria: {ctx['name']}")
        sys.exit(1)

    audit_res = auditor.audit_retraction(targets, ctx)
    print(format_audit_report(audit_res))

    if args.apply:
        delete_doc = args.delete_doc or (args.institution is not None)
        apply_retraction(
            bundle_dir,
            audit_res,
            action_ungrounded=args.action_ungrounded,
            delete_container_doc=delete_doc,
            substitute_id=args.substitute_id,
            substitute_url=args.substitute_url,
            substitute_title=args.substitute_title
        )
    else:
        print("💡 Dry-run analysis complete. No files were modified.")
        target_flag = ""
        if args.source:
            target_flag = f"--source {args.source}"
        elif args.url:
            target_flag = f"--url '{args.url}'"
        elif args.institution:
            target_flag = f"--institution {args.institution}"
        elif args.doc:
            target_flag = f"--doc {args.doc}"
        elif args.domain:
            target_flag = f"--domain {args.domain}"

        print("   To execute this retraction and archive all assets, run:")
        print(f"   python3 scripts/backout_source.py {target_flag} --apply --action-ungrounded {args.action_ungrounded}\n")


if __name__ == "__main__":
    main()
