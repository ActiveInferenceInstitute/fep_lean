"""Extra GaussRunner branches: controlled Hermes results and error paths (no direct execution)."""

from __future__ import annotations

import pytest
from pathlib import Path

from catalogue.topics import FEPTopicCatalogue, TopicEntry
from gauss.client import OpenGaussClient
from gauss.runner import GaussRunner, TopicRunResult
from llm.hermes import HermesConfig, HermesExplainer, HermesResult
from verification.lean_verifier import LeanVerifier

PROJ = Path(__file__).resolve().parent.parent


class FixedHermes(HermesExplainer):
    """Returns a fixed result without HTTP (overrides ``explain_topic`` only)."""

    def __init__(self, result: HermesResult) -> None:
        super().__init__(HermesConfig(enabled=True, api_key="test-key-not-used"))
        self._fixed = result

    def explain_topic(self, topic: TopicEntry, *, preamble: str = "") -> HermesResult:  # type: ignore[override]
        return self._fixed


class BoomClient(OpenGaussClient):
    def create_session(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("simulated session failure")


def _topic() -> TopicEntry:
    c = FEPTopicCatalogue.from_yaml(PROJ / "config" / "topics.yaml")
    return c.topics[0]


def test_run_topic_no_refined_sketch(tmp_path: Path) -> None:
    lean = LeanVerifier(PROJ / "lean", PROJ)
    hermes = FixedHermes(
        HermesResult(
            success=True,
            model_used="fixture",
            explanation="ok",
            refined_lean_sketch="",
            topic_id="x",
        )
    )
    client = OpenGaussClient(gauss_home=tmp_path / "g")
    runner = GaussRunner(lean, hermes, client, PROJ)
    r = runner.run_topic(_topic())
    assert r.status == "no_lean_sketch"
    assert r.success is False


def test_run_topic_with_reasoning_turn(tmp_path: Path) -> None:
    lean = LeanVerifier(PROJ / "lean", PROJ)
    sketch = "theorem fixtureReason : True := True.intro\n"
    hermes = FixedHermes(
        HermesResult(
            success=True,
            model_used="fixture",
            explanation="e",
            refined_lean_sketch=sketch,
            reasoning="internal chain",
            tokens_used=3,
            topic_id="x",
        )
    )
    client = OpenGaussClient(gauss_home=tmp_path / "g")
    runner = GaussRunner(lean, hermes, client, PROJ)
    r = runner.run_topic(_topic())
    assert r.topic_id == _topic().id
    assert r.hermes_success is True


def test_run_topics_batch_catches_runner_exception(tmp_path: Path) -> None:
    lean = LeanVerifier(PROJ / "lean", PROJ)
    hermes = HermesExplainer(HermesConfig(enabled=False))
    client = BoomClient(gauss_home=tmp_path / "g")
    runner = GaussRunner(lean, hermes, client, PROJ)
    t = _topic()
    out = runner.run_topics_batch([t])
    assert len(out) == 1
    assert out[0].success is False
    assert "Unhandled runner exception" in out[0].error


def test_run_topic_closes_session_after_unexpected_error(tmp_path: Path) -> None:
    lean = LeanVerifier(PROJ / "lean", PROJ)
    hermes = HermesExplainer(HermesConfig(enabled=False))
    client = OpenGaussClient(gauss_home=tmp_path / "g")
    runner = GaussRunner(lean, hermes, client, PROJ)

    def explode(*_args, **_kwargs):
        raise RuntimeError("injected failure after session creation")

    runner._record_hermes_turns = explode  # type: ignore[method-assign]
    with pytest.raises(RuntimeError, match="injected failure"):
        runner.run_topic(_topic())
    rows = client._conn.execute("SELECT status FROM sessions").fetchall()
    assert [row["status"] for row in rows] == ["error"]


# ── Explicit workflow selection tests ────────────────────────────────────────

def test_workflow_draft_preserves_requested_stage(tmp_path: Path) -> None:
    lean = LeanVerifier(PROJ / "lean", PROJ)
    hermes = FixedHermes(
        HermesResult(success=False, model_used="fixture", topic_id="fep-001")
    )
    client = OpenGaussClient(gauss_home=tmp_path / "g")
    runner = GaussRunner(lean, hermes, client, PROJ)
    result = runner.run_topic(_topic(), workflow="draft")
    assert result.workflow == "draft"


def test_workflow_prove_preserves_requested_stage(tmp_path: Path) -> None:
    lean = LeanVerifier(PROJ / "lean", PROJ)
    hermes = FixedHermes(
        HermesResult(success=False, model_used="fixture", topic_id="fep-001")
    )
    client = OpenGaussClient(gauss_home=tmp_path / "g")
    runner = GaussRunner(lean, hermes, client, PROJ)
    result = runner.run_topic(_topic(), workflow="prove")
    assert result.workflow == "prove"


# ── Hermes caching tests ──────────────────────────────────────────────────────

class _CountingHermes(HermesExplainer):
    """Hermes fixture that counts calls and returns a compile-clean sketch."""

    def __init__(self) -> None:
        self._cfg = HermesConfig(enabled=False, api_key="")
        self.call_count = 0

    def explain_topic(self, topic: TopicEntry, *, preamble: str = "") -> HermesResult:  # type: ignore[override]
        self.call_count += 1
        return HermesResult(
            success=True,
            model_used="fixture",
            explanation="fixture explanation",
            refined_lean_sketch="theorem fixtureCached : True := True.intro\n",
            topic_id=topic.id,
        )


def test_run_topic_uses_cache_on_second_call(tmp_path: Path) -> None:
    """Second identical run returns from SQLite cache; explain_topic called only once."""
    lean = LeanVerifier(PROJ / "lean", PROJ)
    hermes = _CountingHermes()
    client = OpenGaussClient(gauss_home=tmp_path / "g")
    runner = GaussRunner(lean, hermes, client, PROJ)
    topic = _topic()

    runner.run_topic(topic)
    runner.run_topic(topic)

    assert hermes.call_count == 1


def test_stage_results_empty_for_verify(tmp_path: Path) -> None:
    """verify workflow always produces an empty stage_results list."""
    lean = LeanVerifier(PROJ / "lean", PROJ)
    hermes = FixedHermes(
        HermesResult(success=False, model_used="fixture", topic_id="fep-001")
    )
    client = OpenGaussClient(gauss_home=tmp_path / "g")
    runner = GaussRunner(lean, hermes, client, PROJ)
    result = runner.run_topic(_topic(), workflow="verify")
    assert result.stage_results == []


# ── Review workflow stage_results test ───────────────────────────────────────

def test_run_topic_review_workflow_populates_stage_results(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """workflow='review' appends a 'review_commentary' entry to stage_results
    when the refined sketch compiles successfully."""
    monkeypatch.setenv("FEP_LEAN_GAUSS_WORKFLOWS", "1")

    lean = LeanVerifier(PROJ / "lean", PROJ)
    # A sketch that will compile so verify_res.compiles is True (triggers review pass)
    compile_sketch = "theorem fixtureReview : True := True.intro\n"
    hermes = _CountingHermes()

    client = OpenGaussClient(gauss_home=tmp_path / "g")
    runner = GaussRunner(lean, hermes, client, PROJ)
    if not runner.lean.check_lake_available():
        pytest.skip("pinned Lake is unavailable")
    result = runner.run_topic(_topic(), workflow="review")

    assert result.workflow == "review"
    assert len(result.stage_results) == 1
    assert result.stage_results[0]["stage"] == "review_commentary"
    assert "success" in result.stage_results[0]
    # Review Hermes call is also cached — first call was verify, second is review_commentary
    assert hermes.call_count == 2


# ── Error capture tests ──────────────────────────────────────────────────────


def test_topic_run_result_error_uses_skip_reason_when_errors_empty(
    tmp_path: pytest.fixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When verify_res.errors is empty but compilation fails (timeout/no-lake),
    the runner must populate error from skip_reason or stdout rather than empty string."""
    monkeypatch.setenv("FEP_LEAN_GAUSS_WORKFLOWS", "1")

    lean = LeanVerifier(PROJ / "lean", PROJ)
    hermes = _CountingHermes()
    client = OpenGaussClient(gauss_home=tmp_path / "g")
    runner = GaussRunner(lean, hermes, client, PROJ)

    topic = _topic()
    result = runner.run_topic(topic)

    # The result should have a non-empty error string when lean_compiles is False
    if not result.lean_compiles:
        assert result.error != "", (
            "TopicRunResult.error must be non-empty when lean compilation fails; "
            "got empty string — check runner.py error fallback chain"
        )
