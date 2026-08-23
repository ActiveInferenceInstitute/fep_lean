# Formalism catalogue 120 visual acceptance

Review date: 2026-08-21
Browser: Chrome 151.0.7922.169
Verdict: accepted on all six final captures

The final atlas and numerical workbench were regenerated from the canonical
120-topic presentation join, loaded from local `file://` URLs in headless
Chrome, exercised through their real DOM controls, and captured at standalone,
desktop, and narrow/mobile sizes. No network asset was requested.

## Final captures

| Surface | Dimensions | SHA-256 | Verdict |
| --- | ---: | --- | --- |
| `assets/atlas-120-standalone.png` | 1600×1094 | `46ea33440e3cf77e1197c7a1a700f27d239bd8807b7d76d85ab9ff782d5a72f0` | Accepted |
| `assets/atlas-120-desktop.png` | 1440×22948 | `10b5713cd009bef94efe0aca7df0be5618863a18fe35e3b2b59a30e145218d41` | Accepted |
| `assets/atlas-120-mobile.png` | 390×1812 | `a3c29b23ee6bce0bf420ab31f047ffa8207605d51f840ecc53c2d0b4d83adf76` | Accepted |
| `assets/dashboard-120-standalone.png` | 1600×1688 | `bc48756fd916135bc7e2c00369fff1fefe641139cbce92d7a8782c6575e4072d` | Accepted |
| `assets/dashboard-120-desktop.png` | 1440×11308 | `26802580da156905cc0bc20aa84a238f05eb9618dd2b47732d49164f62b05add` | Accepted |
| `assets/dashboard-120-mobile.png` | 390×3258 | `2ca9cc6518e3763667d804ea1a332948f44fc73202f7b3427845ec2db5503a8d` | Accepted |

## Interaction receipt

[`assets/browser-interaction-receipt.json`](assets/browser-interaction-receipt.json)
is the machine-readable Chrome receipt (`accepted: true`, SHA-256
`fd85d27a162172853ec064256bd630baf385cb89fead6332265ea81c990ece3e`).
It pins:

- 120 topic rows and 98 relation rows;
- relation conservation at 20 `formal`, 70 `formal_pairing`, and 8
  `conceptual` rows;
- 5 areas, 15 families, and the exact 34-topic FEP and 7-topic learning-family
  filters;
- search, select filters, `/` focus, and `Escape` reset behavior;
- all 10 witness workbenches and accessible tables;
- 9 theorem instances and 1 explicitly labeled structural analogue;
- six zero-baseline bar groups in each embedded desktop/mobile overview;
- complete responsive summaries at 390 CSS pixels, no page-level horizontal
  overflow, and no external assets.

## Independent image-only review

A fresh, unprimed reviewer inspected only the six final PNGs. It accepted every
surface with no visible clipping, severed cards, illegible wrapped labels, or
count mismatch. It also confirmed that plot domains, extrema or baselines,
legends, residuals, and tolerances remain visible, and that every evidence
boundary explicitly distinguishes deterministic diagnostics from both Lean
proof evidence and empirical validation.

The screenshots and DOM receipt are validation artifacts, not theorem receipts
or empirical evidence for the Free Energy Principle.
