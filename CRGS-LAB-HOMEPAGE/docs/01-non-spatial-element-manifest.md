# Non-Spatial Element Manifest (Qi149-layout CRGS Lab)

Every element is named. No element is described by a screen position. The words top, bottom, left, right, above, below, center, and side do not appear. The "Verify" column describes what the screen presents, by content and behavior only.

## Frame
| Element ID | Role | Verify (non-spatial) |
|---|---|---|
| `Site-Header` | Persistent bar over the page. | A bar that stays in view while content moves. Over the hero it is transparent; once the page moves it becomes a solid cream bar. |
| `Brand-Mark` | The CRGS Lab mark + wordmark. | The stacked mark next to the wordmark "CRGS Lab". Selecting it returns to the start. |
| `Primary-Nav` | The named navigation links. | Monospace uppercase links: Lab, Stack, Programs, Publications, Contact. |
| `Header-Meta` | The lab descriptor line. | Monospace text "Runtime-first · since 2026 / Founder · Corey Alejandro". |
| `Menu-Toggle` | The two-line control that opens the fullscreen menu. | A two-line (hamburger) control. Selecting it opens `Overlay-Menu`. |
| `Overlay-Menu` | The fullscreen menu. | A dark fullscreen panel with six numbered links (01–06) and a "Close" control. |
| `Footer-Identity-Bar` | The closing identity band. | A dark band with four labeled columns, an oversized "CRGS Lab" watermark, and a copyright line. |

## Hero
| Element ID | Role | Verify (non-spatial) |
|---|---|---|
| `Hero-Slider` | The fullscreen rotating hero. | A full-viewport region with a photographic background that changes on its own. |
| `Hero-Slide-01` | Constitutional slide. | Eyebrow "01 — Constitutional Legitimacy"; headline "Governance, not observation." ("observation" italic sand); a ghost "Read the mission" pill. |
| `Hero-Slide-02` | Runtime slide. | Eyebrow "02 — Runtime Enforcement"; headline "Six layers, one discipline."; a ghost "Explore the stack" pill. |
| `Hero-Slide-03` | Instructional slide. | Eyebrow "03 — Instructional Integrity"; headline "Is the instruction sound?"; a ghost "See the programs" pill. |
| `Hero-Dots` | The slide indicators. | A row of short marks; the active mark is sand-colored. |
| `Hero-Prev` / `Hero-Next` | The slide controls. | Two round outline controls that change the slide. |

## Sections
| Element ID | Role | Verify (non-spatial) |
|---|---|---|
| `Mission-Band` | The mission region. | Eyebrow "The Lab · Canonical"; a large serif mission statement; a monospace positioning note. |
| `Six-Layer-List` | The numbered stack. | Six rows. Each row has a number (01–06), a layer name, and a one-line description. Pointing at a row inverts it to dark. |
| `Layer-Row-01`…`Layer-Row-06` | The six layers. | Rows named Constitutional Legitimacy, Governance Specification, Runtime Enforcement, Instructional Integrity, Human-Centered Experience, Digital Twin Applications. |
| `Programs-Grid` | The seven-program grid. | Seven tiles. Each tile has a ghost number, a layer label, and a program title. Pointing at a tile turns it terracotta and reveals "View program". |
| `Program-Tile-01`…`Program-Tile-07` | The seven programs. | One tile per program (see Parity Mapping). |
| `Counters-Band` | The statistics band. | A terracotta band with four numbers that count up: 06, 07, 4,025, 62/62. |
| `Publications-Band` | The publications cards. | Three cards, each with a kind label, a title, and a "Read" link. |
| `CTA-Band` | The closing call to action. | A dark photographic band with "Open a case with the lab." and one ghost pill. |

## Status pills (revealed in detail pages)
`status · ratified` (green), `status · active` (copper), `status · in study` (amber), `status · open` (coral).
