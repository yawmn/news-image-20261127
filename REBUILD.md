# REBUILD — news-image-20261127, map-only (skill v4.3.0), Fri 27 Nov 2026

Resubmission of "THE GLOBAL DISPATCH — Friday 27 November 2026".
Supersedes submission 01a21ba2 (13:12 WIB, same day). Only the map
changed; every other part of the page is byte-identical to the
submitted version (diff-verified: broadsheet.html differs only in
the map SVG block, the `.mapleg` font size, and the SPREAD legend).

## What changed

- Map rebuilt with the map-design renderer (zetxek/map-design, MIT)
  per skill v4.3.0 §6: real Natural Earth coastline + country
  borders (Equal Earth), 7 on-map pins by real lon/lat, 6 spread
  pins (Europe 3, NZ 3) with leader lines to their true positions.
- Recoloured to the broadsheet palette (sea #dcebf0, land #e8dcbc).
- SPREAD legend now names all 6 spread pins (Brussels added).
- `.mapleg` font 20px → 16px so the 6-pin legend fits on one line.

## Geometry correction (important)

The v4.3.0 map rules were written assuming the map panel is
504×300px at final size. It is not. Measured from the live page
(`.mapbox` 940×365, `.mapbox svg` 910×270 at 3000px scale): the
real panel is **311×92px at final size**. A full world map in that
panel caps pins at ~7px and labels at ~7px at final size — the
skill's 11–13px pin / 12px label targets are geometrically
unachievable here (they would need a viewBox that crops out the
southern hemisphere). The skill needs a v4.3.1 correction; this
rebuild records the measured maxima instead of pretending.

Deviations from the rebuild brief, all driven by the corrected
geometry (brief assumed 1518×912 panel / 504×300 final):
- radius 32, labelSize 60 (not 20/38) — to reach 7.1px pins and
  6.7px labels at final size in the real panel.
- viewBox cropped to the map content + NZ band
  ("43 142.4 1432 660") so the map fills the 910×270 box
  (meet scale 0.409, up from 0.291 uncropped).
- NZ spread row at y=760 (not 830 — outside the crop).
- Spread spacing 120 units (not 80 — the number labels collided
  with the next dot at 80).
- `.mapleg` 16px (not 20px — the 6-pin legend wrapped to 2 lines
  at 20px and 18px, shrinking the map).

## Measurements (final size, from the SVG + live page)

- Pin diameter: 7.0px → 7.1px at final (meet 0.409).
- Pin labels ("N Place"): 6.7px at final.
- Base pin edge gaps: smallest Seoul–Tokyo 0.0px (dots touch,
  separated by their white strokes; labels on opposite sides).
  All other pairs ≥8.4px.
- Renderer report: 0 of 7 base labels dropped. All 6 spread pins
  recovered via SPREAD legend + number labels beside their dots.
- Leader lines cross near the NZ islands (true positions 19 units
  apart; spread order reverses the true west–east order). Cosmetic;
  dots and numbers stay readable.
- ALSO columns end level (bottom-y spread 0px at 3000px scale).
- Entry: 1024×1024, 768,065 bytes, sha256
  a538157cee98b69d5ab4125b184bfe0980409b69db3e7e791e79e7b9b12aa949.
- Determinism: `repo/main.py --self-test` twice byte-identical,
  mode 0644, same sha256.

## QC gate (v4.3.0 §9)

- #1 thumbnail PASS — dense broadsheet at 256px.
- #2 density PASS — scenes unchanged from the submitted version.
- #3 ALSO PASS — spread 0px.
- #4 map PASS with recorded deviation — renderer-built, real
  coastline/borders, NZ drawn, continents recognisable at
  thumbnail, spread + legend, zero unrecovered dropped labels,
  no label/pin overlap; px targets (11–13px pins, 12px labels)
  NOT met — panel-capped at 7.1px/6.7px, see geometry note above.
- #5 timeline PASS — AROUND THE WORLD fallback, unchanged.
- #6 text PASS — no typos; spread numbers beside dots, not inside.
- #7 ledger PASS — 31/31 URLs, date gate clean, 20 source domains,
  swaps A–D, rejected 37.
- #8 deterministic PASS — see above.
- #9 strips PASS — count line, key figures, date-check strip,
  HOW SURE chips unchanged.
- #10 brief PASS — brief-v410.md + this note; ledger frozen.
- #11 blind test PARTIAL — builder is ledger-aware; no
  ledger-blind reader available.
- #12 colour PASS — fills unchanged; map sea/land/pins distinct
  at thumbnail.
- #13 word caps PASS — headlines unchanged; map labels ≤3 words.
- #14 count line PASS — "31 STORIES · 9 REGIONS · 13 SCENES ·
  ALL FROM FRIDAY 27 NOVEMBER 2026" matches the ledger.
- #15 submit status — see below.

Tally: 14 PASS / 1 PARTIAL (#11) / 0 FAIL.
