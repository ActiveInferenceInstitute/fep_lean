# OpenGauss and SQLite

Full mode requires the `gauss` executable and a successful `gauss doctor`.
`OpenGaussClient` is the local SQLite persistence layer used for sessions,
turns, response cache entries, artifacts, and operation logs.

State is stored under `GAUSS_HOME` (default `~/.gauss`). Artifact publication is
atomic and database rows include the exported file hash. Use a temporary
`GAUSS_HOME` for isolated development and inspect `get_stats()` before cleanup.
