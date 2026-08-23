# itskaero Landing Page — v2

Interactive static landing page for the itskaero project archive.

## What changed in v2

This version moves beyond a card-based portfolio and uses the design concept:

**problem → take apart → find patterns → build → result**

### Interactive pieces

- Cursor-following hero interaction
- Animated orbit / data-field details
- Scroll-revealed process steps
- Project constellation with category filters
- Project-specific visual scenes
  - MeritNama: candidates / preferences / quotas / seats / allocation
  - Nabz: prescription-paper scene with bilingual treatment
  - Antibiome / Antibiotigram: microbiology / susceptibility visualization
  - Nigheban / BahawalpurNama: system/data experiments
- Five-step project story timeline
- Project-specific "next project" transitions
- Responsive mobile layout
- `prefers-reduced-motion` fallback
- No framework or build step

## Deploy

Put `index.html`, `style.css`, and `script.js` in the root of the GitHub Pages repository.

## Important

The visual scenes are deliberately lightweight representations, not screenshots. The next production pass can replace them with actual screenshots, SVG reconstructions, or live mini-interactions from each product.

The project URLs are already wired to the `itskaero.github.io` pages and `itskaerox` GitHub repositories used by the archive. Update any URL if a project moves.

## Suggested next production pass

1. Capture real product screenshots.
2. Replace generic scenes with project-specific SVG/canvas interactions.
3. Add scroll-progress-driven transitions between the five story stages.
4. Add Open Graph image + favicon.
5. Add a subtle page-load intro, but keep it skippable and fast.
6. Add project metadata from a local JSON file so the archive is easy to maintain.
