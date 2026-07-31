# FEP Lean Agents — `config/` (project root)

**Version**: v1.0.0 | **Status**: Active | **Last Updated**: July 2026

## Purpose

The `config/` directory contains the YAML configuration files that drive the
`fep_lean` pipeline and its maintained theorem review. Runtime settings and
catalogue bodies remain separate from the semantic audit.

## Files

| File | Description |
|------|-------------|
| `settings.yaml` | All runtime configuration: GAUSS_HOME, model, Hermes AI layer |
| `topics.yaml` | 50 FEP/AI/IG/BM/TD topic definitions (id, area, mathlib, mathlib_status, nl, lean_sketch, `latex_equations` — one string per `theorem` in the sketch) |
| `theorem_maturity.yaml` | Maintained semantic review of each topic's primary theorem; rendered to `docs/theorem-maturity-audit.md` |

## `settings.yaml` — Key Sections

Shipped defaults match [`settings.yaml`](settings.yaml); if this section lags, **trust the YAML**.

### `project`
| Key | Default | Description |
|-----|---------|-------------|
| `name` | `fep_lean` | Project identifier |
| `version` | `1.0.0` | Semantic version |
| `description` | (see YAML) | Human description |

### `gauss`
| Key | Default | Env Override | Description |
|-----|---------|-------------|-------------|
| `home` | `~/.gauss` | `GAUSS_HOME` | Root dir for sessions, artifacts, logs |
| `default_model` | `moonshotai/kimi-k2.6` | `GAUSS_DEFAULT_MODEL` | Default OpenRouter model id for sessions |
| `log_level` | `INFO` | `GAUSS_LOG_LEVEL` | Logging verbosity |
| `source` | `fep_lean` | — | Session source tag for filtering |
| `verify_lean` | `true` | — | When Gauss workflows run, invoke `lake env lean` per topic |

### `hermes`
| Key | Default | Env Override | Description |
|-----|---------|-------------|-------------|
| `enabled` | `true` | — | Enable Hermes when workflows run |
| `model` | `moonshotai/kimi-k2.6` | — | Primary OpenRouter model ID (Moonshot Kimi K2.6, 262K ctx, fast instruct) |
| `fallback_models` | (list in YAML) | — | Tried in order if primary fails |
| `max_tokens` | `16384` | — | Max tokens (non-reasoning path) |
| `timeout_s` | `150` | — | **Wall-clock** budget (seconds) for non-reasoning models — enforced via worker thread + `join(timeout=…)` in `_make_request` |
| `reasoning_max_tokens` | `65536` | — | Budget for reasoning-style models (Kimi K2.x, GLM-5.1, DeepSeek-R1, o1/o3, Nemotron) |
| `reasoning_timeout_s` | `300` | — | Wall-clock budget for reasoning-style models (same enforcement as `timeout_s`) |

**HTTP retry env (read by `src/llm/hermes.py`, not YAML):**

| Env | Default | Description |
|-----|---------|-------------|
| `HERMES_429_MAX_RETRIES` | `2` | Retries after HTTP 429 before next model |
| `HERMES_NETWORK_MAX_RETRIES` | `2` | Retries after transient transport errors (`IncompleteRead`, `URLError`, etc.) before giving up on the current model |

### Config Priority (highest → lowest)

```
Environment variable (OPENROUTER_API_KEY, GAUSS_HOME, etc.)
    └─ ~/.gauss/.env  (auto-loaded by gauss/client.py)
            └─ config/settings.yaml
                    └─ Code defaults (in llm/hermes.py, gauss/runner.py)
```

## `topics.yaml` — Topic Schema

Each topic record must conform to:

```yaml
topics:
  - id: fep-001                          # unique, format: fep-NNN, NN=001..050
    title: Variational Free Energy Bound  # short human title
    area: FEP                             # one of: FEP | ActiveInference | BayesianMechanics | InfoGeometry | Thermodynamics
    mathlib: >                            # Mathlib4 module paths (comma-separated)
      MeasureTheory, Probability.KL
    mathlib_status: real                 # real | partial | aspirational
    nl: >                                 # Natural-language statement (1-3 sentences)
      The variational free energy F[q,p] ...
    lean_sketch: |                        # Lean4 theorem sketch (multi-line)
      theorem variational_free_energy_bound ...
    latex_equations:                    # one LaTeX block per ``theorem``; see ``theorem_latex_signatures`` + ``SKETCHES`` in ``scripts/catalogue_sketches.py`` (direct source: ``catalogue_sketches``)
      - "..."                             # (see generated topics.yaml; do not hand-edit the full list)
```

### Area Taxonomy

| Area | Count | Primary Mathlib Modules |
|------|-------|------------------------|
| `FEP` | 14 | MeasureTheory.Measure.MeasureSpace, Analysis.SpecialFunctions.Log.Basic |
| `ActiveInference` | 11 | Algebra.BigOperators.Group.Finset, Data.Fin, Order.Basic |
| `InfoGeometry` | 8 | Analysis.InnerProductSpace.Basic, Topology.MetricSpace.Basic |
| `BayesianMechanics` | 10 | LinearAlgebra.Matrix.Transpose, Data.Finset.Basic |
| `Thermodynamics` | 7 | Analysis.SpecialFunctions.Log.Basic, Analysis.SpecialFunctions.Exp |

### Maturity Distribution (July 2026)

| Status | Count |
|--------|------:|
| ✓ `real` (status) | 50 |
| ⚠ Partial | 0 |
| ○ Aspirational | 0 |

## Operating Contracts

1. **Never commit API keys**: `settings.yaml` must not contain `OPENROUTER_API_KEY`.
2. **topics.yaml is immutable during a run**: Do not modify `topics.yaml` while the pipeline is running.
3. **All 50 topic IDs must be unique** and follow the `fep-NNN` pattern.
4. **Lean sketches MUST be syntactically valid Lean4** (though they may use `sorry` axioms).
5. **Mathlib field annotated with `mathlib_status`** — `real`, `partial`, or `aspirational` per topic, verified against Lean 4 Mathlib periodically.

## Navigation

- **Self**: [AGENTS.md](AGENTS.md)
- **Parent**: [../AGENTS.md](../AGENTS.md)
- **Human README**: [README.md](README.md)
- **Source that reads config**: [../src/AGENTS.md](../src/AGENTS.md)
- **Settings reference**: [README.md](README.md)
