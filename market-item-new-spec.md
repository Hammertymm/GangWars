# Market Item Card Specification v2.1 (Final)

## Overall Card

- Card dimensions: **957px × 548px**
- Existing GW styling remains unchanged:
  - Borders
  - Colours
  - Shadows
  - Backgrounds
  - Typography
  - Corner radius
- Internal padding: **15px** on all outer edges.

# Layout Structure

The card consists of two fixed-width sections:

| Section | Width |
|----------|---------|
| Icon Panel | 518px |
| Content Panel | 409px |

Total card width:

518 + 15 + 409 + 15 = 957px

Both sections share the same usable height:

548 - 15 - 15 = 518px

# Icon Panel

## Position

- Left side of card
- 15px from top
- 15px from left
- 15px from bottom

## Size

518px × 518px

## Image Rules

- Perfect square image area.
- Remove all internal padding.
- Centre icon horizontally and vertically.
- Scale icon to the maximum possible size while maintaining aspect ratio.
- Do not crop.
- Icons should visually occupy most of the available square.
- Large icons are preferred over empty space.

# Content Panel

## Position

- Begins immediately to the right of the icon panel.
- 15px gutter between icon and content areas.

## Size

409px × 518px

# Row 1 — Item Name

## Height

248px

## Margins

- 15px from left edge
- 15px from right edge
- 15px from top edge

## Content

Examples:

MOONSHINE
BATHTUB GIN
AGED SCOTCH
FINE COGNAC

## Rules

- Vertically centred within the row.
- Left aligned.
- Single line only.
- Truncate gracefully if required.

# Row 2 — Price + Stock

## Height

200px

## Layout

Price aligned left.

Stock aligned right.

Example:

$10,582                      0

$89                          0

$38,825                      17

## Rules

- Price and stock sit on the same horizontal baseline.
- Stock quantity replaces the existing "Hold —" text entirely.
- No labels such as HOLD, OWNED, STOCK or Qty.
- Display only the number.
- Number is right aligned against the content panel margin.

# Row 3 — Action Buttons

## Height

140px

## Layout

Two equal-width buttons.

### SELL Button

190px × 140px

Position:

- 15px from content area's left edge.

### BUY Button

190px × 140px

Position:

- 15px from SELL button.
- 15px from content area's right edge.

# Final Visual Layout

┌──────────────────────────────────────────────────────────┐
│                                                          │
│  518×518 ICON   │  ITEM NAME                             │
│                 │                                        │
│                 │                                        │
│                 ├────────────────────────────────────────│
│                 │ $10,582                           0    │
│                 ├────────────────────────────────────────│
│                 │ [ SELL ]     15px      [ BUY ]         │
│                 │                                        │
└──────────────────────────────────────────────────────────┘

## Key Design Goals

1. Maximise icon size.
2. Eliminate wasted space around icons.
3. Keep item names highly readable.
4. Remove "Hold —" placeholder text.
5. Show stock quantity cleanly and minimally.
6. Maintain large touch-friendly BUY/SELL buttons.
7. Preserve the premium 1920s Gang Wars aesthetic.
