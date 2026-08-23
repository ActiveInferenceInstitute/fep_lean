# Formalism catalogue 155 — visual acceptance

The final atlas and numerical dashboard were captured from the canonical HTML
projections with Google Chrome 151.0.7922.169. The browser executable SHA-256
was `aea09d69ce7f24d5901f6bfb15dd44d0c856e793e0a498f8d8393ec7d2c308ec`.
The schema-4 [browser receipt](assets/browser-interaction-receipt.json) binds the
browser, normalized render configuration, observed environment, projection
hashes, six screenshots, exact DOM observations, and replayed interactions.

## Accepted captures

| Capture | SHA-256 |
| --- | --- |
| [`atlas-155-desktop.png`](assets/atlas-155-desktop.png) | `8f9edaa79e02b18a68e2886d88b5c9f2797f2ef211908bcd5c45028c935029a3` |
| [`atlas-155-mobile.png`](assets/atlas-155-mobile.png) | `8696603bd8b51b9ec83e52974190b5812d335eb8b766afe9395a8d1f4b480a0f` |
| [`atlas-155-standalone.png`](assets/atlas-155-standalone.png) | `c4d9f164892548c233ee0c179565966e0050c7416b2fd20d89fc11949749881a` |
| [`dashboard-155-desktop.png`](assets/dashboard-155-desktop.png) | `b00d77b467c6aaee7abf5b8b7523af48d9cc0b2679f747958803553c08372a93` |
| [`dashboard-155-mobile.png`](assets/dashboard-155-mobile.png) | `e9ff61f0ba783aa17e3b2284c8f765e7c8758c9358fb6b9191ffab6bbc97afb3` |
| [`dashboard-155-standalone.png`](assets/dashboard-155-standalone.png) | `9a14f16d40d5fe9c73658cbeecaba53a55a3ad661b3f4ee4b61b52d111f40b7b` |

The previous 120-topic images in
[`formalism-catalogue-120/assets`](../formalism-catalogue-120/assets/) were used
as comparison provenance rather than as pixel-matching targets.

## Review history and decisions

Fresh unprimed reviews rejected earlier candidates for hidden or unwieldy
mobile plot access, undersized metadata, merged Boolean category keys, clipped
labels and footer text, weak inner-scroll affordances, and visually ambiguous
coincident series. The accepted renderer resolves those findings by:

- keeping all 15 plot summaries in five visible, indexed groups of three;
- exposing disclosure and persistent contained-scroll cues;
- fitting long labels and wrapping footer/metadata copy within their cards;
- enlarging axis, legend, and categorical-key typography;
- retaining exact-zero hollow markers so zero is not mistaken for missing data;
  and
- drawing coincident values on one neutral rail with centered ring and diamond
  identities instead of inventing a numerical offset.

The final fresh, context-free critic returned **ACCEPT** for the desktop,
standalone, exact-390 mobile, and expanded-group views. It found no material
clipping, overflow, overlap, or blur. An independent renderer review returned
**CLEAN**. Real-Chrome replay then reproduced the receipt twice with no
validation errors.

The sole optional polish note was to make the desktop sticky-filter backing
fully opaque in scroll-position crops. It was not a correctness, readability,
or containment defect and was left unchanged after the source freeze.

These captures establish presentation and interaction quality only. The exact
tables remain authoritative for numerical values, and neither the screenshots
nor the numerical witnesses constitute formal proof or empirical validation.
