# Glossary

- **Catalogue mode** — deterministic offline validation and artifact generation;
  it reports zero verified topics.
- **Full mode** — strict Hermes, Lean, OpenGauss, and artifact execution.
- **Hermes** — configured HTTP explanation and Lean-refinement client.
- **Lean clean** — Lean compilation succeeds and the source contains no proof
  holes outside comments.
- **OpenGauss** — the configured `gauss` command plus this project's SQLite
  session client; it is not a database server dependency.
- **Run manifest** — JSON record containing mode, capabilities, per-topic
  outcomes, source/configuration digests, and artifact hashes.
