# Crime Ledger UI Blueprint

Authoritative layout specification for the Crime Ledger rebuild. Design canvas: **473×1024** pixels (portrait). Machine-readable rects: [`scripts/ledger-blueprint.json`](../../scripts/ledger-blueprint.json).

Reference PNGs (locked standards): [`docs/ui-standards/ledger-*.png`](./)

## Achievement counts

| Category | Count |
|----------|------:|
| General | 14 |
| Rare | 10 |
| Super Rare | 10 |
| Godlike | 5 |
| Golden Godlike | 1 |
| **Total** | **40** |

## Global structure (all screens)

- **Background:** `#000000`
- **Outer frame:** thin double gold border with rounded corners (baked in PNG)
- **Masthead:** `GANG WARS` serif, centered between horizontal gold rules (baked)
- **Scale:** frame width = `min(100cqw, 100cqh × 473/1024)`; no fluid reflow
- **Safe area:** `#crt.ledger-mode` adds only `env(safe-area-inset-*)` padding
- **Z-order:** base PNG → transparent dynamic text → hit targets

## Typography

| Role | Treatment |
|------|-----------|
| Masthead / screen titles | Serif, gold `#c9a85a` (baked in art) |
| Dynamic counters | Sans-serif, gold `#c9a85a`, transparent background |
| Row counters (home) | Muted gold `#9a8860`, smaller |
| List titles (revealed) | Sans uppercase `#c9a85a` |
| List titles (hidden) | Muted `#6a5e48` |
| Checkmarks | Gold `#c9a85a` |

## Screen: Crime Ledger Home

**Assets:** `crime-ledger-home-base.png` (display), `crime-ledger-home.png` (reference)

**Scroll:** none

### Regions (px)

| Element | x | y | w | h |
|---------|--:|--:|--:|--:|
| Total counter | 130 | 486 | 213 | 18 |
| Row hit: General | 17 | 508 | 439 | 54 |
| Row counter: General | 268 | 542 | 92 | 16 |
| Row hit: Rare | 17 | 562 | 439 | 54 |
| Row counter: Rare | 238 | 594 | 92 | 16 |
| Row hit: Super Rare | 17 | 616 | 439 | 54 |
| Row counter: Super Rare | 318 | 646 | 92 | 16 |
| Row hit: Godlike | 17 | 670 | 439 | 54 |
| Row counter: Godlike | 268 | 698 | 72 | 16 |
| Row hit: Golden Godlike | 17 | 724 | 439 | 54 |
| Row counter: Golden Godlike | 368 | 750 | 52 | 16 |
| Back button | 20 | 934 | 433 | 48 |

### Dynamic copy

- Total: `{found} / 40 FOUND`
- Rows: `{n} / {total}` (no FOUND suffix)

## Screen: General

**Asset:** `ledger-general-base.png`

**Scroll:** list panel only (14 rows × 38px = 532px > panel 528px)

| Element | x | y | w | h |
|---------|--:|--:|--:|--:|
| Counter strip | 60 | 338 | 353 | 28 |
| List panel | 17 | 382 | 439 | 528 |
| Row height | — | — | — | 38 |
| Back | 20 | 934 | 433 | 48 |

**Counter:** `{found} / 14 FOUND`

## Screen: Rare / Super Rare

Same layout as General except row height **53px**, **10 rows**, no scroll.

**Counter:** `{found} OF 10 DISCOVERED`

## Screen: Godlike

Same as Rare but **5 rows**, row height **106px**, no scroll.

**Counter:** `{found} OF 5 DISCOVERED`

## Screen: Golden Godlike

Taller hero; counter and list shifted down.

| Element | x | y | w | h |
|---------|--:|--:|--:|--:|
| Counter strip | 60 | 388 | 353 | 28 |
| List panel | 17 | 432 | 439 | 478 |
| Row height | — | — | — | 72 |
| Back | 20 | 934 | 433 | 48 |

**Counter:** `{found} OF 1 DISCOVERED`

## Achievement detail view

No separate art file. Category screen with `ledgerFocusId` set: scroll row into view, highlight, reveal animation (General: `???` → title).

## Visibility rules

| Category | Locked |
|----------|--------|
| General | `???` |
| Rare+ | padlock icon + `UNKNOWN` (no description) |
| Revealed + unlocked | title + checkmark |

## Validation checklist (per screen)

- [ ] No opaque mask overlays
- [ ] No duplicate counters (baked + DOM)
- [ ] Category labels fully visible on home
- [ ] Counter alignment matches reference slots
- [ ] No scroll on home; scroll only in General list panel
- [ ] No overflow/clipping
- [ ] Back button hit zone matches art

## Discrepancy log

| Date | Screen | Issue | Resolution |
|------|--------|-------|------------|
| 2026-06-16 | Home | Wide black masks covered category labels | Rebuild: `-base.png` + transparent `.ledger-counter` slots |
| 2026-06-16 | All | Reference example achievements visible | Category `-base.png` inpaints list panel; DOM rows only show `???`/`UNKNOWN` until revealed |
| 2026-06-16 | All | Duplicate counters | Dynamic text only on counter-free base assets |
