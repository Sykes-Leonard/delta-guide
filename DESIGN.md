---
type: Concept
title: "DELTA Guide: Visual Design System & UI Specification"
description: "The **DELTA Guide Concept Mind Map Browser** embodies a synthesis of two foundational traditions:"
status: draft
generated:
  by: agent:antigravity
  at: 2026-10-02T04:32:16Z
verified: []
---

# DELTA Guide: Visual Design System & UI Specification

---

## 1. Design Philosophy & Heritage Synthesis

The **DELTA Guide Concept Mind Map Browser** embodies a synthesis of two foundational traditions:
1. **St. Francis High School (Mountain View)**: Franciscan humanism, intellectual warmth, hospitality, and contemplative clarity—grounded in the school's heritage colors of **"Leather"** (warm rich espresso), **"Sunlight"** (radiant academic gold), **"Cedar"** (warm academic terracotta), and **"Dove"** (crisp, warm parchment white).
2. **The University of Notre Dame & The DELTA Network**: Collegiate academic rigor, the iconic **"Notre Dame Navy"** (`#0C2340`) and **"Dome Gold"** (`#C99700`), the dynamic **"DELTA Ember Orange"** (`#F26430`), and a vibrant multi-color spectrum symbolizing diverse disciplines convening for the common good.

Rather than a cold, sterile Silicon Valley cyberpunk theme, the aesthetic of the DELTA Guide is **"Luminous Digital Personalism"**: an elegant, warm-toned dark canvas that feels like a sacred illuminated manuscript brought to life with hardware-accelerated fluid motion.

```
       [St. Francis High School]                   [University of Notre Dame / DELTA]
     Franciscan Warmth & Community                 Collegiate Rigor & Ethical Vision
     • Leather (Rich Warm Espresso)                 • Notre Dame Navy (#0C2340)
     • Sunlight (Academic Gold)                     • Dome Gold (#C99700)
     • Cedar (Warm Terracotta)                      • DELTA Ember Orange (#F26430)
     • Dove (Parchment White)                       • Multi-color Five-Pillar Spectrum
                   │                                             │
                   └──────────────────────┬──────────────────────┘
                                          │
                                  [DELTA Guide UI]
                             Luminous Digital Personalism
                 Dark Warm Canvas • Jewel-Toned Nodes • Glassmorphism
```

---

## 2. Design Tokens & Color Palette

### 2.1 Surface & Neutral Foundations (Dark Canvas)
The dark background avoids pure, desaturated `#000000` or sterile slate grays, subtly infusing warm espresso undertones:

| Token Name | Hex Code | Semantic Role |
| :--- | :--- | :--- |
| `--surface-canvas` | `#0E1118` | Root viewport backdrop (deep midnight with subtle warm tint) |
| `--surface-panel` | `rgba(20, 24, 35, 0.85)` | Glassmorphic floating sidebars and HUD controls (`backdrop-blur-md`) |
| `--surface-drawer` | `rgba(18, 22, 32, 0.94)` | Slide-over detail drawer with warm micro-border |
| `--surface-card` | `rgba(27, 32, 48, 0.65)` | Individual concept matrix cards and detail sections |
| `--border-subtle` | `rgba(255, 255, 255, 0.08)` | Structural dividers and neutral card strokes |
| `--border-warm` | `rgba(229, 168, 35, 0.22)` | Accentuated borders highlighting active or hovered elements |

### 2.2 Heritage Brand Tokens
* **St. Francis Sunlight Gold**: `#E5A823` — Used for primary interactive triggers, active tab states, and the Flourishing cluster.
* **Notre Dame Dome Gold**: `#C99700` — Used for badges, crest borders, and verified trust indicators.
* **Notre Dame Navy**: `#0C2340` — Deep brand backdrop accent for headers, primary badges, and control anchors.
* **DELTA Ember Orange**: `#F26430` — Energy accent for CTA buttons, the central Delta mark, and relational edge highlights.
* **Franciscan Leather**: `#2B1810` / `#3D2314` — Warm dark substrate for card hover backgrounds and subtle gradients.
* **Dove Parchment**: `#F7F4EE` — High-contrast primary text (`--text-primary`), softer than harsh pure white.
* **Muted Cream**: `#C4BDAB` — Secondary text, metadata subtitles, and inactive icon states.

### 2.3 Thematic Cluster Chromatic Palette
Each of the five thematic clusters radiates with a dedicated jewel-toned color signature:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 THEMATIC CLUSTERS                                      │
├─────────────────────────┬──────────────┬──────────────┬────────────────────────────────┤
│ Cluster Name            │ Base Color   │ Glow Accent  │ Meaning / Pillar Alignment     │
├─────────────────────────┼──────────────┼──────────────┼────────────────────────────────┤
│ 🔴 Central Anchor       │ `#E53E3E`    │ `#FEB2B2`    │ Human Dignity (Imago Dei)      │
│ 🟡 Human Flourishing    │ `#E5A823`    │ `#FBD38D`    │ Eudaimonia, Character, Virtue  │
│ 🔵 Moral Agency         │ `#3182CE`    │ `#90CDF4`    │ Conscience, HITL, Labor        │
│ 🟣 Power & Governance   │ `#805AD5`    │ `#D6BCFA`    │ Distributive Justice, Swarms   │
│ 🟢 Embodiment & Presence│ `#38A169`    │ `#9AE6B4`    │ Incarnation, Sacred Presence   │
│ 🟠 Transcendence & Truth│ `#DD6B20`    │ `#FBD38D`    │ Babel vs Jerusalem, Sabbath    │
└─────────────────────────┴──────────────┴──────────────┴────────────────────────────────┘
```

---

## 3. Typography & Editorial Hierarchy

To bridge technological agility with philosophical depth, the typography uses a pairing of high-legibility geometric sans-serif for UI mechanics and a classical warm serif for philosophical headings:

```css
/* UI Mechanics & Body */
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* Philosophical Concepts & Classical Headings */
--font-serif: 'Newsreader', 'Georgia', 'Merriweather', serif;

/* Monospace Metadata, Code & Latency Tokens */
--font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', monospace;
```

### Typographic Scales:
* **H1 Concept Hero Title**: `font-serif font-bold text-2xl tracking-tight text-[var(--dove)]` (e.g. *Phronesis (Practical Wisdom)*)
* **Cluster Badges**: `font-mono uppercase text-xs tracking-widest font-semibold`
* **Executive Summary / Thesis**: `font-sans text-sm leading-relaxed text-[#D6CEBE]`
* **Relational Verb Chips**: `font-mono text-xs px-2 py-0.5 rounded-full font-medium`

---

## 4. SPA Layout & Component Architecture (`/viewer/`)

The SPA follows a single-screen responsive viewport (`100vw`, `100vh`) with fixed viewport management, preventing awkward browser scrollbars while maximizing canvas real estate.

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│  HEADER: [▲ DELTA Guide]  [Search Concepts...]  [Clusters ▾] [Views: 🌐 📑 🏛️]   [Theme] │
├────────────────────────┬─────────────────────────────────────────────────┬───────────────┤
│                        │                                                 │               │
│  LEFT SIDEBAR          │  CENTRAL INTERACTIVE CANVAS                     │  SLIDE-OVER   │
│  (300px)               │                                                 │  DRAWER       │
│  • Cluster Filter      │  • Central Crimson Node: Human Dignity          │  (460px)      │
│    Checkboxes          │  • 5 Radiant Cluster Constellations             │               │
│  • Tag Filter Cloud    │  • Smooth Bezier Directed Edges                 │  • Overview   │
│  • Institutional Slices│  • Hover Tooltips with Relationship Verbs       │  • Edges      │
│  • Graph Metrics:      │                                                 │  • Provenance │
│    28 Nodes, 129 Edges │                                                 │  • Pedagogy   │
│                        │                                                 │               │
│                        ├─────────────────────────────────────────────────┤  (Animates in │
│                        │  FLOATING HUD CONTROLS                          │  on node click│
│                        │  [Zoom + -] [Reset] [Physics: ON/OFF] [Depth]   │  keeps canvas │
│                        │                                   [Mini-Map]    │  active)      │
└────────────────────────┴─────────────────────────────────────────────────┴───────────────┘
```

### 4.1 Header Bar
* **Brand Logo**: Combined mark featuring the Franciscan Tau / Holy Cross subtle geometry integrated with Notre Dame’s golden Delta emblem.
* **Global Omni-Search**: Instant keyboard-accessible (`Cmd+K` or `/`) fuzzy search querying concept titles, executive summaries, and primary sources.
* **View Switcher Tabs**:
  * 🌐 **Constellation View** (Interactive physics network graph)
  * 📑 **Matrix Card Grid** (Organized categorical card view grouped by cluster)
  * 🏛️ **Institutional Lens** (Filter nodes by source: Vatican, Notre Dame, Oxford, Harvard, DeepMind, UN)

### 4.2 Left Filter Sidebar
* **Cluster Checklist**: Interactive pills with color dot indicators and node counters (`Human Flourishing (6)`, `Moral Agency (5)`, etc.). Clicking solo-filters that cluster.
* **Relationship Verb Filter**: Filter visible edges by relationship category:
  * *Foundational* (`Grounds`, `Requires`, `Affirms`)
  * *Tensions & Threats* (`Threatened by`, `Opposes`, `Erodes`)
  * *Remedies & Scaffolding* (`Remedied by`, `Cultivates`, `Forges`)
  * *Statutory & Governance* (`Mandates`, `Enforces`, `Codifies`)
* **Quick Stats Counter**: Live count of visible nodes and active edges.

### 4.3 Central Graph Canvas
* **Engine**: Hardware-accelerated HTML5 Canvas with fluid force simulation.
* **Physics & Layout Mode**:
  * **Mode A (Default)**: Free force-directed graph with auto-stabilization (Barnes-Hut simulation settling into organic equilibrium).
  * **Mode B (Concentric / Radial Orbits)**: Concentric rings locking Human Dignity at $(0,0)$ with clusters orbiting radially.
* **Micro-Interactions**:
  * **Hover Node**: Adjacent edges brighten to 100% opacity; non-connected nodes dim to 25%. A small tooltip displays the node's 1-line thesis.
  * **Click Node**: Camera smoothly glides to center on the node, highlights all immediate 1-hop neighbors, and opens the Right Slide-Over Drawer.

### 4.4 Right Slide-Over Drawer
* Width: `460px`, slides in smoothly from the right with `cubic-bezier(0.16, 1, 0.3, 1)`.
* Keeps the main graph canvas visible and operable in the remaining viewport.
* **Four Tab Sections**:
  1. **Overview Tab**: Full concept thesis, OKF trust status (`stable`), tags, and primary cluster badge.
  2. **Relational Edges Tab**: Two distinct interactive card stacks:
     * *Outbound Edges*: Connected concept card + relationship verb tag (e.g. `Remedied by` $\rightarrow$ `Cognitive Friction`). Clicking flies camera to target node!
     * *Inbound Edges*: Shows which concepts point into this node.
  3. **Institutional Provenance Tab**: Verified badges for contributing institutions (Notre Dame ECG, Oxford AI Ethics, Harvard HFP, DeepMind Institute), with direct external links to papers and reports.
  4. **St. Francis Pedagogy Tab**: Concrete classroom and institutional guidelines for educators, addressing student formation, cognitive friction preservation, and ethical software constraints.
* **Footer Actions**: Direct button to view raw Markdown document in knowledge base or copy link.

### 4.5 Floating HUD & Controls
* Positioned bottom-center with frosted glass styling:
  * Zoom In (`+`), Zoom Out (`-`), Center Camera (`⛶`).
  * **Physics Freeze Switch**: Pauses dynamic force calculations to lock the canvas in place for study.
  * **Neighborhood Depth Slider**: Toggle between `1-Hop` (direct connections only) and `2-Hop` (extended relational web).
  * **Mini-Map**: Bottom-right interactive preview showing canvas boundaries and viewport rectangle.

---

## 5. Matrix / Card Grid View Specification

For users who prefer a linear, editorial browsing experience:
* Top bar features filter chips for each cluster.
* 3-column responsive card grid.
* Cards feature frosted glass styling (`bg-[#161B26]`, border `rgba(255,255,255,0.06)`).
* Cards display:
  * Glowing cluster indicator pill.
  * Bold title and 2-sentence thesis.
  * Edge counters: `X Outbound | Y Inbound`.
  * Institutional grounding badges.
  * **"Inspect in Graph"** button that switches to Constellation View and centers the camera on that node.

---

## 6. Motion & Animation Principles

All transitions adhere to physical metaphors of mass, dignity, and calm:
* **Camera Pan/Zoom**: Smooth spring dynamics (duration: `750ms`, easing: `cubic-bezier(0.25, 1, 0.5, 1)`).
* **Node Glow Pulse**: Subtle sinusoidal breathing animation on the central `Human Dignity` node (`duration: 3.5s`, `opacity: 0.4` to `0.85`).
* **Drawer Entry/Exit**: Horizontal slide (`transform: translateX(0)`) with backdrop blur transition.

---

## 7. Accessibility & Performance Standards

1. **Contrast Ratio**: All body copy meets **WCAG 2.1 AA** standards ($\ge 4.5:1$ contrast against surface background).
2. **Keyboard Navigation**:
   * `Cmd + K` or `/`: Focus search input.
   * `Escape`: Close detail drawer / reset selection.
   * `Tab` / `Shift+Tab`: Traverse drawer edge chips and control buttons.
3. **Zero External Build Step**: The SPA in `/viewer/` will run as a pure, self-contained web app with zero npm dependencies, using clean native browser APIs and embedded graph libraries.
