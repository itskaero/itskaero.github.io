# NAMA — the design system of the nama family

> **One skeleton, one accent each.**

Live spec: **https://itskaero.github.io/nama/**
Stylesheet: **https://itskaero.github.io/nama/nama.css**

Members: MeritNama · medNAMA · Nabz · Antibiome · Antibiotogram

---

## Why this exists

It wasn't designed up front. Three projects built independently had already landed on:

- the same easing curve — `cubic-bezier(.2, .8, .2, 1)`
- a cool, slightly blue-green off-white for ink, never `#fff`
- a near-black blue ground (`#04060c` in MeritNama, `#000912` in medNAMA)
- IBM Plex Sans for UI, IBM Plex Mono for anything that is a precise value
- an accent in the green→cyan band

That is not coincidence any more, it's a dialect. This writes it down so the next
project starts there instead of re-deriving it.

---

## The mechanism

Everything structural is shared. A family member differs by **one attribute**:

```html
<body data-accent="meritnama">   <!-- mint   #2FE39A -->
<body data-accent="mednama">     <!-- peach  #EBD5BE -->
<body data-accent="nabz" data-register="clinical">
```

Components only ever read `--accent`, `--accent-2`, `--accent-wash`, `--accent-ink`
and `--accent-glow`. Because they resolve to colour properties that already have
transitions, swapping the attribute **animates** the whole re-tint for free. No JS,
no theme objects, no build step.

---

## Tokens

| group | tokens |
|---|---|
| **ground** | `--nama-void #04070E` · `--nama-deep #080D16` · `--nama-panel #0D1420` · `--nama-raised #121B29` |
| **ink** | `--nama-ink #EEF3F4` · `--nama-ink-2` 70% · `--nama-ink-3` 44% · `--nama-ink-4` 22% · `--nama-line` 10% · `--nama-line-soft` 5.5% |
| **signals** | mint `#2FE39A` · cyan `#4DB8D9` · sky `#56AAE2` · peach `#EBD5BE` · rose `#D39794` · teal `#19A06D` · amber `#D9A24A` · alert `#E0716A` |
| **type** | `--nama-serif` Instrument Serif · `--nama-sans` IBM Plex Sans · `--nama-mono` IBM Plex Mono · `--nama-urdu` Noto Nastaliq Urdu |
| **scale** | `--t-display` → `--t-micro`, all `clamp()`, one scale from phone to desk |
| **space** | `--s-1` 4px → `--s-10` 140px, 4px base |
| **radius** | `--r-1` 8 · `--r-2` 14 · `--r-3` 22 · `--r-4` 30 · `--r-pill` 999 |
| **motion** | `--ease` · `--ease-out` · `--ease-liquid` · `--t-fast` 160 · `--t-base` 260 · `--t-slow` 440 · `--t-cine` 900 |

Radii span Nabz's 8px instruments through medNAMA's 22px panels, so both ends of the
family sit inside one scale.

---

## Two registers

**void** (default) — dark, calm, data-forward. Dashboards, analytics, night reading.
MeritNama and medNAMA live here.

**clinical** (`data-register="clinical"`) — near-white, trust-forward. Instruments used
at speed by an expert, and documents a patient has to read. Nabz lives here.

Light is Nabz's mandatory default and is never auto-switched from the OS: dark murders
Nastaʿlīq legibility and costs clinical trust. Dark exists there only as an explicit
user choice.

---

## Primitives

```
type        .nama-display  .nama-h1  .nama-h2  .nama-h3  .nama-lede
            .nama-mono  .nama-eyebrow  .nama-urdu  .nama-ltr
controls    .nama-btn (--solid --ghost --quiet)  .nama-pill (--accent)
            .nama-live  .nama-link
surfaces    .nama-card  .nama-panel  .nama-glass-plate  .nama-hr
            .nama-grain  .nama-grid-bg
data        .nama-stat (__num __lab)
states      .nama-state (--ok --warn --danger)
motion      .nama-reveal [data-delay]  .nama-words .w
layout      .nama-page  .nama-section  .nama-band
```

---

## The rules that actually bind

A token file is easy to follow. These take discipline.

- **Colour means something or isn't used.** Accent = action and emphasis. Teal = vetted.
  Amber = unverified. Red = danger. Everything else is ink.
- **Red is never decorative.** If red appears where it isn't danger, it stops meaning
  danger — and then it fails where it matters.
- **Spend boldness in exactly one place per screen.** One element carries the eye.
- **Encode state in more than one channel.** Glyph + border + label. Colour reinforces,
  never carries. Mono printers and colourblind readers get the same message.
- **No third typeface.** The serif-against-Plex contrast *is* the personality.
- **Monospace means a precise value.** Doses, IDs, ranks, counts. Never in prose, and
  never inside patient-facing Urdu.
- **Isolate LTR tokens inside RTL lines** (`.nama-ltr`). A reordered dose is a safety
  bug, not a cosmetic one.
- **Every animated primitive has a correct still state.** Under
  `prefers-reduced-motion` the page is *finished*, not frozen mid-entrance.
- **Never the cream-paper cliché.** Warm beige for "document" reads as generic. Warmth
  comes from the in-palette peach and rose.

---

## Using it

```html
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://itskaero.github.io/nama/nama.css">
```

```html
<body data-accent="mednama">
  <div class="nama-grain"></div>
  <p class="nama-eyebrow">Learn from the source</p>
  <h1 class="nama-display">Practice with purpose.</h1>
  <a class="nama-btn nama-btn--solid" href="#">Open</a>
</body>
```

Adding a member: append one `[data-accent="…"]` block to §2 of `nama.css` with its five
accent variables. Nothing else.
