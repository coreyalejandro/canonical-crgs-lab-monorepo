# Native-Divi note

The earlier version of this kit offered a "native Divi modules" path. The redesigned site is **interaction-rich** — a fullscreen auto-advancing hero slider, a fullscreen overlay menu, and animated counters. None of those can be reproduced with native page-builder widgets.

So there is now **one path**: paste the global CSS once, then build each page as a single **Code module** holding that page's markup. This is what `03-build-guide-divi.md` describes. It is simpler and reproduces the mockup exactly.

If a future page is plain content (text and images only, no slider or menu behavior), it can be built with native Divi modules and styled by the same global CSS — give each section a CSS class from the design system (for example `ip-section`, `kv`, `repo`, `callout`). But the Home page and the shared header, menu, and footer should stay as Code-module markup.
