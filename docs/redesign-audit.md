# KAERO: audit before the Systems Atlas redesign

Audit date: 22 October 2026. Every claim below was checked against the public repository,
its README, or the live deployment on that date.

## 1. The current site

| | |
|---|---|
| Stack | Static HTML + CSS + vanilla JS. No build step, no package.json, no workflow. |
| Deployment | GitHub Pages, served from the repository root of the default branch (no `.github/workflows`). |
| Pages | `/` (homepage) and `/nama/` (the NAMA design-system spec). |
| Shared CSS | `nama/nama.css` is used by the homepage **and** documented as a public stylesheet other projects link to (`https://itskaero.github.io/nama/nama.css`). It must not move or change. |
| JS | `script.js` has a spring "liquid" carousel, scroll reveals, a word-by-word statement, nav state, and a progress bar. |
| Anchors in use | `#family`, `#system`, `#how`, `#about`, `#top`. |
| Images | `banner.png` (1536×1024, 1.6 MB, used only as `og:image`). `background.jpg` (2048×1152) is not referenced anywhere. |
| Fonts | Instrument Serif, IBM Plex Sans, IBM Plex Mono (Google Fonts). |

What works: the reduced-motion handling is careful, the carousel is keyboard-accessible, and the
NAMA system is a real, documented asset.

What's weak:
- Dark void + accent glow + carousel cards looks like a product launch page, not a person.
- The hero has three stat tiles ("5 projects live", "13 induction cycles", "1 design system") that
  say nothing about the thinking behind the work.
- Several facts are out of date (see §2): Antibiome is no longer a culture-surveillance web app,
  and there's no `antibiotigram` repository.
- The process section is a plain list, and the about copy repeats the hero.
- None of the projects shows its real interface.

## 2. Verified projects

| Brief name | Reality on 22 Oct 2026 | Public? | Live | Last push | Use |
|---|---|---|---|---|---|
| MeritNama | Residency-induction analytics for Punjab: merit tables, predictor, calculator, seat-allocation simulator. Inductions 8–21 in `inductions/`. Public landing page; the analytics app sits behind invite-only sign-in. | ✅ repo | ✅ `itskaero.github.io/meritnama/` | 2 Oct | Feature |
| Nabz | Bilingual (English + Nastaʿlīq Urdu) prescription PWA plus a Windows clinic-station `.exe` (v0.2.0). Records stay on the device. | ✅ | ✅ product page + releases | 4 Oct | Feature |
| Antibiome | **Now "Antibiome PICU"**: Electron/React/SQLite desktop app for paediatric intensive care. Admissions, therapy episodes, PIM3, stewardship, cumulative antibiogram, research explorer. Windows builds 0.1.3. The original NICU culture web app is retired to `/legacy/`. | ✅ | ✅ product page + releases | 9 Oct | Feature |
| Antibiotigram | The repo is **`antibiotogram`**; the live page is titled "Antibiotic Hub": spectrum explorer, visual coverage heatmap, combination builder, drug cards. | ✅ | ✅ `itskaero.github.io/antibiotogram/` | 14 Apr | Feature, marked as last updated April |
| Nigheban | No public repository; Pages URL returns 404. | ❌ | ❌ | | Omit |
| BahawalpurNama | No public repository; Pages URL returns 404. | ❌ | ❌ | | Omit as a project; Bahawalpur appears only as an illustrative motif |
| Shaheen | Discord bot + FastAPI + public site for a Pakistani Brawlhalla clan, now **BRAWLISTAN** ("Pakistan's Brawlhalla Network"). The Pages URL redirects to `brawlistan.rekorex.online`. Site data snapshots refresh daily. | ✅ | ✅ | 22 Oct | Feature, under Community & Play |

Found during the audit, not in the brief:

| Project | What it is | Live | Last push | Use |
|---|---|---|---|---|
| medNAMA | Textbook-grounded answers with page citations, recalled FCPS Part 1 papers, re-tests. Invite-only early access, "running with a small group of trainees". App source in `medNAMA-app`, product page in `medNAMA`. | ✅ product page | 22 Oct | **05 / Next experiment** |
| Nisbat | Calm family dashboard for Pakistani households (prayer times, Quran, PBS grocery prices, smog, Urdu listening), on a Chromecast TV and every phone. | ✅ product page | 14 Oct | Feature, under Local Experiments |
| brawlhalla-leaderboard | February 2026 precursor: leaderboard images for Brawlhalla players. | ❌ Pages | 15 Feb | Mentioned inside Shaheen only |

## 3. Reusable visual material (all real, nothing mocked)

| Project | Source | Notes |
|---|---|---|
| MeritNama | Live landing page capture | The in-app screens are behind sign-in, so they can't be captured |
| Nabz | `docs/assets/script.png`, the README's "real output from the PDF renderer" | Cropped to the medication block, without the sample clinician header |
| Antibiome | `desktop/docs/screenshots/*.png`, 19 screenshots on demo data | Microbiology antibiogram and phone census |
| Antibiotogram | Live "Visual" tab capture | Coverage heatmap |
| medNAMA | `assets/shots/*.jpg` | Answer with inline textbook citations, dashboard |
| Nisbat | Live product page capture | |
| BRAWLISTAN | Live rankings page capture | |

## 4. Missing information

- **Contact:** GitHub is the only verified public channel. The old README links `@itskaerox`, which
  looks like a typo, so the site uses `github.com/itskaero` only. No email, booking link, or social
  profile is invented.
- No verified personal biography beyond what the current site and README already say (problem-driven,
  clinician-builder, Python/JavaScript, Pakistan). The Nabz sample sheet carries a clinician name and
  credentials. That's demo output, so the portfolio doesn't treat it as a bio.
- No usage numbers are verified apart from figures the product pages state about their own data.
  The portfolio quotes none of them.

## 5. Implementation plan

- Keep the stack: static HTML/CSS/vanilla JS on GitHub Pages from the repository root. Leave `nama/`
  untouched. Keep `#family`, `#system`, `#how`, `#about` as working anchors.
- Replace the homepage with a seven-chapter narrative (00 Entering → 06 Invitation) under a new
  visual language, **The Systems Atlas**: ivory paper, forest and charcoal plates, signal lime,
  editorial type, mono annotations.
- Generate the illustrations as SVG from one reproducible script (`tools/art/build.py`), so palette,
  line weight and texture stay shared. Convert real captures to WebP.
- One small vanilla script for chapter navigation, reveals, filters and progress. No libraries, no
  WebGL.
