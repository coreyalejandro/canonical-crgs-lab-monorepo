# CRGS Lab — Website Build Kit

**Constitutional Runtime Governance Systems Research Lab.** This kit redesigns the Qi149 template into the CRGS Lab identity, in the design language of coreyalejandro.com, and hands a WordPress (Divi) team everything needed to build it.

Built so **The Free Website Guys can build it in WordPress with Divi** — page structure is native Divi; the look and the creative interactions ride in through one global stylesheet and a few self-contained code blocks.

> **Start here:** open `docs/handoff-brief.html` (a one-page, print-ready brief), then `mockup/index.html` (the design target).

---

## What is inside

```
crgs-lab-website-kit/
├── README.md
├── mockup/
│   ├── index.html                    ← Home (Qi149 layout: fullscreen hero slider, overlay menu)
│   ├── preview.html                  ← COMPLETELY FUNCTIONING click-through preview (single file)
│   ├── 404.html                      ← styled "case not found" page
│   ├── programs/                     ← one page per research program
│   │   ├── index.html  +  program.css (shared styles)
│   │   ├── constitutional-systems.html      governance-specification.html
│   │   ├── runtime-governance.html          instructional-integrity.html
│   │   ├── madmall.html   digital-twins.html   cognitive-safety.html
│   ├── publications/                 ← detail page per publication
│   │   ├── index.html  ccd-preprint.html  proactive-corpus.html
│   │   ├── pre-registration.html  agent-sentinel.html
│   └── speaking/                     ← detail page per talk
│       ├── index.html  observability-to-governance.html
│       ├── instructional-integrity.html  emotionally-legible-governance.html
├── assets/
│   ├── logo/      crgs-logo(.svg/.png), -mono, -white, -black, mark(.svg/512/1024),
│   │              crgs-avatar(512/1024), crgs-avatar-cream(512/1024)
│   │              crgs-logo-animated.svg, crgs-mark-animated.svg, animated-preview.html
│   │              crgs-logo-animated-pulse.svg, crgs-mark-animated-pulse.svg, crgs-spinner.svg
│   ├── favicon/   favicon.svg, .ico, 16/32/48/512 png, apple-touch-icon, favicon-animated.gif
│   └── social/    og-card.svg + og-card.png (1200×630)
├── wordpress/
│   ├── global-custom-css.css         ← ONE block → Divi › Theme Options › Custom CSS (= site.css)
│   └── code-blocks/
│       └── home.html                 ← paste into one Divi Code module (inner pages follow the same pattern)
└── docs/
    ├── handoff-brief.html                  ← one-page, print-ready brief for the builders
    ├── brand-one-sheet.html                ← logo formats, palette, type, usage rules
    ├── 01-non-spatial-element-manifest.md  ← Phase 1: every element, named, no positions
    ├── 02-parity-mapping.md                ← Phase 2: research content → element IDs
    ├── 03-build-guide-divi.md              ← Phase 3: deterministic build (code-module path)
    ├── 04-build-guide-divi-native.md       ← Phase 3 variant: native Divi modules
    └── 05-github-push-walkthrough.md       ← create the repo and push this kit
```

## Build path

- **One path — `docs/03`.** Paste the global CSS once, then build each page as a single Code module holding that page's markup. The whole look — the hero slider, the fullscreen overlay menu, and the counters — travels inside the markup. `docs/04` explains why the native-module path is retired for this interaction-rich design.

## How the design survives a WordPress build

1. Paste **one** global stylesheet (`global-custom-css.css` = `assets/site.css`) into Divi Theme Options.
2. Build each page as **one Code module** holding that page's markup (from `mockup/`).
3. Upload the logo, favicon, and the five hero images to the Media Library and swap their URLs.
The look, the slider, the fullscreen menu, and the counters all travel inside the markup.

## Pages included

- **Home** (`mockup/index.html`) — the full single-page experience.
- **7 program pages** + a programs index, plus a one-file **programs explorer** for quick click-through.
- **4 publication** detail pages + index, **3 speaking** detail pages + index.
- A styled **404** page.
- A **completely functioning preview** (`mockup/preview.html`): one file that links every page through a working hash router — nav, program cards, publications, talks, 404, the six-layer stack, Reviewer Mode, and the kernel bar all work.

## Brand assets

- **Logo:** color, one-color, **white-on-dark**, **black-on-transparent**, mark-only (SVG + 512/1024 PNG).
- **Avatars:** square dark and cream tiles at 512 and 1024 (for social profiles).
- **Favicon:** `favicon.svg` / `favicon.ico` + sizes; `apple-touch-icon.png`.
- **Social card:** `og-card.png` (1200×630) for Open Graph / link previews.
- **Animated logo:** `crgs-logo-animated.svg` and `crgs-mark-animated.svg` — the runtime axis draws in and the node pops on load, with a reduced-motion fallback. See `animated-preview.html`.
- **Pulse variants:** `crgs-logo-animated-pulse.svg` / `crgs-mark-animated-pulse.svg` add a slow, low-amplitude runtime-node pulse (off under reduced motion).
- **Loader + animated favicon:** `crgs-spinner.svg` (in-page loading spinner) and `favicon-animated.gif` (animated browser-tab icon).
- **Brand one-sheet:** `docs/brand-one-sheet.html` — every logo format, palette swatches with hex, type system, clear space, and usage do/don'ts (print-ready).

## Accessibility commitments built in

- Every interaction is keyboard reachable with a clear text label.
- No flashing or strobing motion; `prefers-reduced-motion` disables transitions.
- Elements are referenced only by unique names — never by screen position — across the mockup, the CSS, and every guide.

## The identity, in one sentence

Corey Alejandro is an AI Safety Research Engineer and Instructional Systems Researcher building Constitutional Runtime Governance Systems that govern the behavior of AI agents, learning systems, digital twins, and human-centered AI environments during execution.

---

*Design language extracted from coreyalejandro.com and the coreyalejandro-portfolio repository. Built as a self-contained handoff package.*
