# Build Guide — WordPress · Divi (Qi149-layout CRGS Lab)

This builds the CRGS Lab site in WordPress with Divi. The Free Website Guys recommend Divi, so Divi is the single build path.

The design is interaction-rich (a fullscreen hero slider, a fullscreen overlay menu, animated counters). That kind of behavior cannot be reproduced with native page-builder widgets, so the whole look and behavior travel inside **one global stylesheet** plus **one Code module per page**. This keeps the build short and exact.

## Rules this guide obeys
1. **No positions.** No element is described as top, bottom, left, right, above, below, center, or side. Elements are named.
2. **One action per step.** Each numbered step asks for one action and states one outcome.
3. **No choices.** One path. Follow the steps in order.
4. **Verify every step.** Each step ends with a `Verify:` line describing what the screen presents.

## Divi control glossary (named by icon)
- **Grey plus icon** — adds a Module.
- **Gear icon** — opens the settings of the element it belongs to.
- **Green checkmark icon** — saves the open settings.
- **Purple "Save" control** — saves the whole page.

---

# PART A · GLOBAL SETUP (once)

## A1 · Fonts
1. Sign in to the WordPress admin account.
   - Verify: the WordPress dashboard is shown.
2. Select "Divi" in the admin menu.
   - Verify: the Divi submenu is shown.
3. Select "Theme Options".
   - Verify: the Theme Options panel opens.
4. Select the "Integration" tab.
   - Verify: a field labeled "Add code to the < head > of your blog" is shown.
5. Select that field.
   - Verify: a text cursor appears in the field.
6. Type this exact line:
   `<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;1,9..144,300;1,9..144,400&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">`
   - Verify: the field displays the font link.
7. Select "Save Changes".
   - Verify: Theme Options reports the change is saved.

## A2 · Global CSS
1. Select the "General" tab in Theme Options.
   - Verify: a field labeled "Custom CSS" is shown.
2. Open `wordpress/global-custom-css.css` from this kit in a text editor.
   - Verify: the file is open.
3. Select all text in the file.
   - Verify: every character is highlighted.
4. Copy the highlighted text.
   - Verify: the text is on the clipboard.
5. Select the "Custom CSS" field.
   - Verify: a text cursor appears in the field.
6. Paste the copied text.
   - Verify: the field displays the full stylesheet.
7. Select "Save Changes".
   - Verify: Theme Options reports the change is saved.

## A3 · Media (logo, favicon, hero images)
1. Select "Media" in the admin menu.
   - Verify: the Media Library is shown.
2. Select "Add New".
   - Verify: an upload field is shown.
3. Upload `assets/logo/crgs-logo.svg`.
   - Verify: the file "crgs-logo.svg" appears in the library. (If SVG is rejected, upload `assets/logo/crgs-logo.png`.)
4. Upload `assets/favicon/favicon.svg`.
   - Verify: the file "favicon.svg" appears in the library.
5. Upload `assets/hero/hero-1-constitutional.jpg`.
   - Verify: the file appears in the library.
6. Upload `assets/hero/hero-2-runtime.jpg`.
   - Verify: the file appears in the library.
7. Upload `assets/hero/hero-3-human.jpg`.
   - Verify: the file appears in the library.
8. Upload `assets/hero/hero-4-archive.jpg`.
   - Verify: the file appears in the library.
9. Upload `assets/hero/hero-5-auditorium.jpg`.
   - Verify: the file appears in the library.
10. Select "Divi" then "Theme Customizer" then "General Settings" then "Site Identity", and set the Site Icon to favicon.svg.
    - Verify: the Customizer previews the favicon as the site icon.

# PART B · THE HOME PAGE

1. Select "Pages" in the admin menu.
   - Verify: the Pages list is shown.
2. Select "Add New".
   - Verify: a new empty page editor opens.
3. Select the "Title" field.
   - Verify: a text cursor appears in the Title field.
4. Type `CRGS Lab Home`.
   - Verify: the Title field displays "CRGS Lab Home".
5. Select "Use Divi Builder".
   - Verify: the Divi builder loads.
6. Select "Build From Scratch".
   - Verify: an empty Divi canvas is shown.
7. Select the grey plus icon.
   - Verify: a module chooser with a search field is shown.
8. Type "Code" into the search field.
   - Verify: the chooser presents the "Code" module.
9. Select the "Code" module.
   - Verify: an empty Code module is created. Its settings panel opens to the "Code" field.
10. Open `wordpress/code-blocks/home.html` from this kit in a text editor.
    - Verify: the file is open.
11. Select all text in the file.
    - Verify: every character is highlighted.
12. Copy the highlighted text.
    - Verify: the text is on the clipboard.
13. Select the "Code" field.
    - Verify: a text cursor appears in the "Code" field.
14. Paste the copied text.
    - Verify: the "Code" field displays the full home markup.
15. In the "Code" field, replace `../assets/hero/hero-1-constitutional.jpg` with the Media Library URL of hero-1-constitutional.jpg.
    - Verify: the first hero image reference now reads as a full Media Library URL.
16. Replace `../assets/hero/hero-2-runtime.jpg` with its Media Library URL. (It appears twice — in the second hero slide and in the CTA band.)
    - Verify: both hero-2 references now read as Media Library URLs.
17. Replace `../assets/hero/hero-3-human.jpg` with its Media Library URL.
    - Verify: the third hero image reference now reads as a Media Library URL.
18. Select the green checkmark icon.
    - Verify: the settings panel closes.
19. Select the purple "Save" control.
    - Verify: the builder reports the page is saved.

# PART C · INNER PAGES (repeat for each)

Each inner page is built the same way: one Code module holds the whole page. The page files are in this kit under `mockup/`.

Inner pages to create (Title — source file in the kit):
- `Research Programs` — mockup/programs/index.html
- `Constitutional Systems Engineering` — mockup/programs/constitutional-systems.html
- `Governance Specification Systems` — mockup/programs/governance-specification.html
- `Runtime Governance Systems` — mockup/programs/runtime-governance.html
- `Instructional Integrity Science` — mockup/programs/instructional-integrity.html
- `Human-Centered Governance Environments` — mockup/programs/madmall.html
- `Constitutional Digital Twins` — mockup/programs/digital-twins.html
- `Cognitive Safety & Human-AI Reliability` — mockup/programs/cognitive-safety.html
- `Publications` — mockup/publications/index.html (plus each publication file)
- `Speaking` — mockup/speaking/index.html (plus each talk file)

For one inner page:
1. Select "Pages" then "Add New".
   - Verify: a new empty page editor opens.
2. Type the page Title from the list.
   - Verify: the Title field displays that title.
3. Select "Use Divi Builder".
   - Verify: the Divi builder loads.
4. Select "Build From Scratch".
   - Verify: an empty Divi canvas is shown.
5. Add a Code module (grey plus icon, search "Code", select it).
   - Verify: a Code module is created.
6. Open the matching source file in a text editor.
   - Verify: the file is open.
7. Copy everything inside its `<body>` tag (the header, the page content, the footer, and the closing script).
   - Verify: that text is on the clipboard.
8. Paste it into the "Code" field.
   - Verify: the field displays the page markup.
9. Replace any `../../assets/hero/...` image reference with the matching Media Library URL.
   - Verify: each hero reference now reads as a Media Library URL.
10. Select the green checkmark icon.
    - Verify: the settings panel closes.
11. Select the purple "Save" control.
    - Verify: the builder reports the page is saved.

Repeat Part C for every page in the list.

# PART D · PUBLISH AND VERIFY

1. Select "Exit Visual Builder".
   - Verify: the standard editor is shown.
2. Select "Publish".
   - Verify: WordPress reports the page is published.
3. Select "View Page".
   - Verify: the CRGS Lab Home page is shown, with the hero image and the headline.
4. Wait until the hero changes on its own.
   - Verify: a second hero slide presents itself.
5. Select the `Menu-Toggle` (the two-line menu control named in the manifest).
   - Verify: a dark fullscreen menu presents itself with six named links.
6. Select "Close".
   - Verify: the fullscreen menu leaves view.
7. Open Settings then Reading then "Your homepage displays" then "A static page", and set the homepage to "CRGS Lab Home".
   - Verify: the Reading settings report "CRGS Lab Home" as the homepage.

**Build complete.** The published site matches `mockup/index.html`.

> The nav inside the header is built into the code block, so a WordPress menu is optional. If you also want a WordPress menu, build one under Appearance → Menus with the same link names.
