---
type: Reference
title: "Visual Design System & Concept Mind Map Specification"
description: "Visual design system, UI layout specification, color tokens, and graph interaction contracts for the Concept Mind Map & Knowledge Graph browser."
tags: [design-system, ui-spec, concept-graph, mind-map, visualization]
status: stable
generated:
  by: agent:antigravity
  at: 2026-10-02T00:00:00Z
verified:
  - by: human:architecture-lead
    at: 2026-10-02T00:00:00Z
---

# Visual Design System & Concept Mind Map Specification

---

## 1. Design Philosophy & Visualization Architecture

The **Concept Mind Map & Knowledge Graph Browser** (`/viewer/index.html`) is an interactive, zero-dependency, and 100% offline-capable single-page application. It renders the living concept ontology, thematic clusters, and typed relational edges defined across the Open Knowledge Format repository.

Rather than a sterile, flat list of documents, the Mind Map provides:
1. **Cluster Constellations**: Concepts gravitationally clustered around thematic domains.
2. **Directed Relational Edges**: Visualizing directional dependencies (*Grounds*, *Requires*, *Operationalized as*, *Tension with*, *Counteracts*).
3. **Progressive Disclosure**: A persistent canvas overview with an animated slide-over drawer for deep node inspection without losing context.

```
       [Thematic Clusters]                         [Relational Edge Matrix]
    Constituent Concept Nodes                     Typed Directional Relationships
    • Grouped by Domain                           • Grounds / Requires
    • Chromatic Palette Identification            • Operationalized as / Implements
    • Lifecycle Indicators (Draft/Stable)         • Tension with / Counteracts
                   │                                             │
                   └──────────────────────┬──────────────────────┘
                                          │
                               [Concept Graph SPA]
                         (/viewer/index.html + D3 Canvas)
                  Dark Canvas • Jewel-Toned Nodes • Slide-over Drawer
```

---

## 2. Design Tokens & Color Palette

### 2.1 Surface & Neutral Foundations (Dark Canvas)

| Token Name | Hex / Value | Semantic Role |
| :--- | :--- | :--- |
| `--surface-canvas` | `#0E1118` | Root viewport backdrop (deep midnight neutral) |
| `--surface-panel` | `rgba(20, 24, 35, 0.85)` | Glassmorphic floating sidebars and HUD controls (`backdrop-blur-md`) |
| `--surface-drawer` | `rgba(18, 22, 32, 0.94)` | Slide-over detail drawer with micro-border |
| `--surface-card` | `rgba(27, 32, 48, 0.65)` | Individual concept matrix cards and detail sections |
| `--border-subtle` | `rgba(255, 255, 255, 0.08)` | Structural dividers and neutral card strokes |
| `--border-warm` | `rgba(229, 168, 35, 0.22)` | Accentuated borders highlighting active or hovered elements |

### 2.2 Text & Content Tokens
* **Primary Text**: `#F7F4EE` — High-contrast, warm off-white.
* **Secondary Text**: `#C4BDAB` — Subtitles, metadata keys, and inactive icon states.
* **Muted Text**: `#718096` — Edge labels and technical metadata.

### 2.3 Thematic Cluster Chromatic Palette

Each thematic cluster is assigned a distinct jewel-toned chromatic signature:

| Cluster Role / Palette | Base Color | Glow Accent | Border Stroke | Semantic Anchor |
| :--- | :--- | :--- | :--- | :--- |
| **🔴 Central Anchor** | `#E53E3E` | `#FEB2B2` | `#9B2C2C` | Foundational Grounding Node |
| **🔵 Azure / Blue** | `#3182CE` | `#90CDF4` | `#2B6CB0` | Architecture & Governance |
| **🟡 Sunlight Gold** | `#E5A823` | `#FBD38D` | `#B7791F` | Core Capabilities & Quality |
| **🟣 Amethyst Violet** | `#805AD5` | `#D6BCFA` | `#6B46C1` | Intelligent Automation & Dispatch |
| **🟢 Emerald Forest** | `#38A169` | `#9AE6B4` | `#2F855A` | Infrastructure & Resilience |
| **🟠 Sunset Bronze** | `#DD6B20` | `#FBD38D` | `#C05621` | Security & Compliance |

---

## 3. Typography & Editorial Hierarchy

```css
/* UI Mechanics & Body */
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* Conceptual Headings & Classical Editorial */
--font-serif: 'Newsreader', 'Georgia', 'Merriweather', serif;

/* Monospace Metadata, Code & Schema Contracts */
--font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', monospace;
```

---

## 4. SPA Layout & Component Architecture (`/viewer/`)

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│  HEADER: [▲ Knowledge Base]  [Search Concepts...]  [Clusters ▾] [Views: 🌐 📑]    [Theme] │
├────────────────────────┬─────────────────────────────────────────────────┬───────────────┤
│                        │                                                 │               │
│  LEFT SIDEBAR          │  CENTRAL INTERACTIVE CANVAS                     │  SLIDE-OVER   │
│  (300px)               │                                                 │  DRAWER       │
│  • Cluster Filter      │  • Thematic Cluster Constellations              │  (460px)      │
│    Checkboxes          │  • Smooth Directed Relational Edges             │               │
│  • Tag Filter Cloud    │  • Hover Tooltips with Relationship Verbs       │  • Overview   │
│  • Graph Metrics:      │                                                 │  • Edges      │
│    Nodes, Edges        │                                                 │  • Provenance │
│                        ├─────────────────────────────────────────────────┤  (Animates in │
│                        │  FLOATING HUD CONTROLS                          │  on node click│
│                        │  [Zoom + -] [Reset] [Physics: ON/OFF]           │  keeps canvas │
│                        │                                                 │  active)      │
└────────────────────────┴─────────────────────────────────────────────────┴───────────────┘
```

### 4.1 Header Bar
* **Omni-Search (`Cmd+K`)**: Instant fuzzy search across concept titles, executive summaries, tags, and relationship descriptions.
* **View Switcher**:
  * 🌐 **Constellation View**: Interactive D3 force-directed physics graph.
  * 📑 **Matrix Card Grid**: Categorical card view grouped by cluster.

### 4.2 Slide-Over Detail Drawer
* Opens smoothly upon clicking any concept node without unloading the canvas.
* Displays:
  - Document title, description, and status tag.
  - Full executive summary.
  - Interactive Inbound and Outbound Relational Edge list (clicking a related concept navigates to that node).
  - Primary source citations.

---

## 5. Relational Edge Grammar

To maintain conceptual rigor, edges must use canonical relationship verbs:

| Verb Category | Canonical Verbs | Color Accent | Description |
| :--- | :--- | :--- | :--- |
| **Foundational** | `Grounds`, `Requires`, `Affirms` | Azure / Gold | Structural or theoretical dependencies. |
| **Operational** | `Operationalized as`, `Implements`, `Enforces` | Emerald | How concepts translate into active production code and SOPs. |
| **Dialectical** | `Tension with`, `Opposes`, `Threatened by` | Ember Orange | Competing architectural paradigms, trade-offs, or risks. |
| **Remedial** | `Remedied by`, `Counteracts`, `Scaffolds` | Teal / Purple | Mitigations, defensive patterns, or pedagogical scaffolding. |
