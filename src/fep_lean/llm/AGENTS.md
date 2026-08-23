# Hermes client contract

This folder owns configuration resolution, request construction, bounded retry
and fallback policy, provider response parsing, and structured LLM results. It
does not compile Lean, write SQLite sessions, or decide full-run claim
readiness.

## Invariants

- Importing the module performs no request and reads no credential.
- Never log, serialize, or return an API key.
- Validate key/provider affinity before sending a request.
- Bound per-model retries, fallback attempts, response size, socket timeouts,
  and the full wall-clock request.
- Keep transient transport failure, rate limiting, non-retryable HTTP failure,
  empty content, and parse failure distinguishable.
- Preserve the model actually used and whether a result came from cache.
- Do not copy the fallback roster into agent documentation; live configuration
  and source own it.
- A refined code block is candidate source, not proof. The Gauss/verification
  layers own compilation and provenance.

## Focused gates

```bash
uv run pytest tests/test_hermes_comprehensive.py \
  tests/test_hermes_error_paths.py \
  tests/test_hermes_explainer.py -q --no-cov
```

Live provider tests require an explicitly supplied credential and are not part
of ordinary local acceptance.
