# Bibliography {#sec:bibliography}

References are in `manuscript/references.bib`. Inline `[@key]` resolved by Pandoc citeproc during rendering. See `docs/_generated/canonical_facts.md` for pipeline status.

<!-- Citation groups — auto-synced to manuscript/references.bib (60 entries, all cited).
     Grouping mirrors the `% ──` section headers in the bib file; rebuild with
     `uv run python -c "from pathlib import Path; import re; …"` if it drifts.

  Free Energy Principle (2)
    friston2006free            — Friston, Kilner & Harrison 2006: A free energy principle for the brain
    friston2010free            — Friston 2010: The free-energy principle: a unified brain theory?

  Renormalization Group & FEP (1)
    friston2019free            — Friston 2019: A free energy principle for a particular physics

  Recent FEP (1)
    friston2005theory          — Friston 2005: A theory of cortical responses

  Active Inference (3)
    friston2017active          — Friston, FitzGerald, Rigoli, Schwartenbeck & Pezzulo 2017: Active Inference — A Process Theory
    parr2022active             — Parr, Pezzulo & Friston 2022: Active Inference (MIT Press)
    sajid2021active            — Sajid, Ball, Parr & Friston 2021: Active inference demystified and compared

  Expected Free Energy & Epistemic Value (1)
    friston2015epistemic       — Friston, Rigoli, Ognibene, Mathys, Fitzgerald & Pezzulo 2015: Active inference and epistemic value

  Generalized Free Energy (1)
    parr2019generalised        — Parr & Friston 2019: Generalized free energy and active inference

  Active Inference Toolkits (1)
    heins2022pymdp             — Heins, Millidge, Demekas et al. 2022: pymdp — A Python library for active inference (JOSS)

  Bayesian Mechanics (6)
    dacosta2023bayesian        — Da Costa, Parr, Sajid, Veselic, Neberath & Friston 2023: Active inference on discrete state-spaces
    dacosta2024bayesian        — Da Costa, Friston, Heins & Pavliotis 2024: Bayesian mechanics of synaptic learning under the FEP
    sakthivadivel2023bayesian  — Sakthivadivel 2023: On Bayesian mechanics — a physics of and by beliefs
    friston2024path            — Friston, Da Costa et al. 2023: Path integrals, particular kinds, and strange things (BibTeX key friston2024path)
    friston2016active          — Friston, FitzGerald, Rigoli, Schwartenbeck, O'Doherty & Pezzulo 2016: Active inference and learning
    toobysmith2024             — Tooby-Smith 2024: Formalization of physics index notation in Lean 4

  Path Integral Formulations (2)
    friston2008variational     — Friston, Trujillo-Barreto & Daunizeau 2008: DEM — A variational treatment of dynamic systems
    friston2021stochastic      — Friston, Fagerholm et al. 2021: Stochastic chaos and Markov blankets

  Markov Blankets & Computational Anatomy (1)
    parr2018markov             — Parr, Da Costa & Friston 2018: Markov blankets, information geometry and stochastic thermodynamics

  Solenoidal Flows & NESS (1)
    ao2004potential            — Ao 2004: Potential in stochastic differential equations — novel construction

  Helmholtz Free Energy (1)
    friston2007variational     — Friston, Mattout, Trujillo-Barreto, Ashburner & Penny 2007: Variational free energy and the Laplace approximation

  Langevin Dynamics & Stochastic Thermodynamics (1)
    pavliotis2014stochastic    — Pavliotis 2014: Stochastic Processes and Applications

  Non-Equilibrium Thermodynamics (4)
    jarzynski1997nonequilibrium — Jarzynski 1997: Nonequilibrium equality for free energy differences (PRL)
    crooks1999entropy          — Crooks 1999: Entropy production fluctuation theorem (PRE)
    landauer1961irreversibility — Landauer 1961: Irreversibility and heat generation in the computing process (IBM JRD)
    prigogine1977nature        — Prigogine & Nicolis 1977: Self-Organization in Nonequilibrium Systems

  Statistical Mechanics and Information Theory (1)
    jaynes1957information      — Jaynes 1957: Information theory and statistical mechanics (Phys Rev)

  Variational Inference (1)
    blei2017variational        — Blei, Kucukelbir & McAuliffe 2017: Variational Inference — A Review (JASA)

  Information Geometry (2)
    amari2016information       — Amari 2016: Information Geometry and Its Applications (Springer)
    amari1998natural           — Amari 1998: Natural gradient works efficiently in learning (Neural Computation)

  Deep Temporal Models (1)
    friston2018deep            — Friston, Parr & de Vries 2018: The graphical brain — belief propagation and active inference

  Precision & Prediction Error (1)
    adams2013predictions       — Adams, Shipp & Friston 2013: Predictions not commands — active inference in the motor system

  FEP Debates and Formalization Gap (3)
    andrews2021math            — Andrews 2021: The math is not the territory
    biehl2021critique          — Biehl, Pollock & Kanai 2021: A technical critique of some parts of the FEP
    aguilera2022particular     — Aguilera, Millidge, Tschantz & Buckley 2022: How particular is the physics of the FEP?

  EFE Debate (1)
    maheu2026reframing         — Maheu, Bhatt, Da Costa et al. 2026: Reframing the Expected Free Energy debate

  Formalization landmarks (4)
    champion2026reframing      — Champion et al. 2026: Reframing the Expected Free Energy — four formulations and a unification
    lean_slt2026               — Lean SLT project 2026: Statistical Learning Theory in Lean 4 / Mathlib4 (work in progress)
    pfr2023lean                — Polynomial Freiman–Ruzsa in Lean 4 (teorth/pfr; arXiv:2311.05762)
    scholze2022liquid          — Scholze & Commelin 2022: Liquid Tensor Experiment (Lean)

  FEP Consciousness Debate (2)
    brainsblog2023             — Beni, Solms, Dołęga et al. 2023: Brains Blog Roundtable — FEP, Consciousness, Realism
    namjoshi2026fundamentals   — Namjoshi 2026: Fundamentals of Active Inference (MIT Press)

  Ecological Psychology (1)
    gibson1979ecological       — Gibson 1979: The Ecological Approach to Visual Perception

  ITPs & Formalization (3)
    leroy2009compcert          — Leroy 2009: Formal verification of a realistic compiler (CompCert)
    moura2021lean              — de Moura & Ullrich 2021: The Lean 4 theorem prover and programming language
    mathlib2020                — Mathlib Community 2020: The Lean mathematical library

  Lean 4 / Theorem Proving (1)
    buzzard2020                — Buzzard, Commelin & Massot 2020: Formalizing perfectoid spaces (POPL)

  LLM–ITP Integration (2 obsolete + 9 modern + 1 follow-on = 12 total)
    first2023draft             — First, Rabe, Ringer & Brun 2023: Baldur — whole-proof generation and repair with LLMs
    trinh2024alphageometry     — Trinh, Wu, Le, He & Luong 2024: AlphaGeometry — solving olympiad geometry without human demonstrations
    yang2024leandojo           — Yang, Swope, Gu et al. 2024: LeanDojo — theorem proving with retrieval-augmented LLMs
    song2025copilot            — Song, Yang & Anandkumar 2025: Lean Copilot
    xin2024lego                — Xin, Guo, Shao et al. 2024: LEGO-Prover — neural theorem proving with growing libraries
    deepseek2024prover         — Xin, Guo, Shao et al. 2024: DeepSeek-Prover — advancing theorem proving via LLMs
    alphaproof2024             — AlphaProof Team / Google DeepMind 2024: AI achieves silver-medal standard at IMO
    jiang2023draft             — Jiang, Welleck, Zhou et al. 2023: Draft, Sketch, and Prove
    avigad2017                 — Avigad, Hölzl & Serafin 2017: A Formally Verified Proof of the CLT (Lean 3 / Mathlib)
    mehtaMetaIT2021            — Mehta, Affeldt, Garrigue & Sakaguchi 2021: A Library for Formalized Information Theory in Isabelle/HOL
    paulson2022thermo          — Paulson 2022: Formalized Statistical Mechanics in Isabelle/HOL (AFP)
    deepseek2025proverv2       — Xin et al. 2025: DeepSeek-Prover-V2
-->

<div id="refs"></div>
