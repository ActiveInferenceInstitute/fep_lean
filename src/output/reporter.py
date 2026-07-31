"""Transactional Markdown and JSON run reports."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from catalogue.topics import FEPTopicCatalogue

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_REQUIRED_REPORT_ARTIFACTS = frozenset(
    {
        "index.md",
        "hermes.md",
        "lean.md",
        "validation.md",
        "verification_manifest.json",
        "run_manifest.json",
    }
)


def _atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(raw, path)
    finally:
        if os.path.exists(raw):
            os.unlink(raw)


def _digest_files(root: Path, paths: Iterable[Path]) -> str:
    """Hash a sorted set of repository files with path names in the digest."""
    digest = hashlib.sha256()
    for path in sorted((Path(path) for path in paths), key=lambda item: str(item)):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        if path.is_file():
            digest.update(path.read_bytes())
        else:
            digest.update(b"<missing>")
        digest.update(b"\0")
    return digest.hexdigest()


def _repository_digest(root: Path, directories: tuple[str, ...], files: tuple[str, ...] = ()) -> str:
    candidates: list[Path] = []
    for directory in directories:
        base = root / directory
        if base.is_dir():
            candidates.extend(path for path in base.rglob("*") if path.is_file())
    candidates.extend(root / relative for relative in files)
    return _digest_files(root, candidates)


def validate_report_receipt(report_root: Path, *, require_complete: bool = False) -> dict[str, Any]:
    """Independently validate a generated report bundle.

    The report's ``summary.json`` is intentionally excluded from its own hash
    map because the map lives inside that file.  This validator therefore
    recomputes every listed artifact hash, rejects path traversal, and
    reconciles the summary, run manifest, and verification manifest.  It does
    not execute Lean, Hermes, OpenGauss, or any other external process.

    ``claim_ready`` is stricter than ``valid``: it is true only for a complete,
    non-empty full-mode receipt whose selected topics all have clean final Lean
    results.  Callers can use ``require_complete=True`` as a policy input while
    still receiving the same structured diagnostics.
    """
    root = Path(report_root).resolve()
    errors: list[str] = []
    checked_artifacts = 0

    def read_json(name: str) -> dict[str, Any] | None:
        path = root / name
        if not path.is_file():
            errors.append(f"missing {name}")
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid {name}: {exc}")
            return None
        if not isinstance(payload, dict):
            errors.append(f"{name} must contain a JSON object")
            return None
        return payload

    if not root.is_dir():
        return {
            "status": "error",
            "valid": False,
            "claim_ready": False,
            "require_complete": require_complete,
            "report_root": str(root),
            "checked_artifacts": 0,
            "errors": [f"report directory is missing: {root}"],
        }

    summary = read_json("summary.json")
    run_manifest = read_json("run_manifest.json")
    verification_manifest = read_json("verification_manifest.json")

    mode = str(summary.get("mode", "")) if summary else ""
    complete = bool(summary.get("complete", False)) if summary else False
    selected_topics = 0
    verified_topics = 0
    summary_rows: list[dict[str, Any]] = []

    if summary is not None:
        if mode not in {"full", "catalogue"}:
            errors.append(f"summary mode is unsupported: {mode!r}")
        if not isinstance(summary.get("complete"), bool):
            errors.append("summary complete must be a boolean")
        raw_selected = summary.get("catalogue_topics")
        if not isinstance(raw_selected, int) or isinstance(raw_selected, bool) or raw_selected < 0:
            errors.append("summary catalogue_topics must be a non-negative integer")
        else:
            selected_topics = raw_selected
        raw_verified = summary.get("verified_topics")
        if not isinstance(raw_verified, int) or isinstance(raw_verified, bool) or raw_verified < 0:
            errors.append("summary verified_topics must be a non-negative integer")
        else:
            verified_topics = raw_verified
        raw_rows = summary.get("topics", [])
        if not isinstance(raw_rows, list) or not all(isinstance(row, dict) for row in raw_rows):
            errors.append("summary topics must be a list of objects")
        else:
            summary_rows = [row for row in raw_rows if isinstance(row, dict)]
        for digest_name in ("source_digest", "config_digest"):
            digest = summary.get(digest_name)
            if not isinstance(digest, str) or not _SHA256_RE.fullmatch(digest):
                errors.append(f"summary {digest_name} must be a lowercase SHA-256 digest")
        if not isinstance(summary.get("toolchain"), dict):
            errors.append("summary toolchain must be an object")

        raw_hashes = summary.get("artifact_hashes")
        if not isinstance(raw_hashes, dict):
            errors.append("summary artifact_hashes must be an object")
            raw_hashes = {}
        seen_artifacts: set[str] = set()
        for raw_relative, expected in raw_hashes.items():
            if not isinstance(raw_relative, str) or not raw_relative:
                errors.append("artifact hash paths must be non-empty strings")
                continue
            relative = Path(raw_relative)
            if relative.is_absolute() or ".." in relative.parts:
                errors.append(f"artifact path escapes report directory: {raw_relative!r}")
                continue
            artifact = (root / relative).resolve()
            if artifact == root or root not in artifact.parents:
                errors.append(f"artifact path escapes report directory: {raw_relative!r}")
                continue
            if not artifact.is_file():
                errors.append(f"hashed artifact is missing: {raw_relative}")
                continue
            if not isinstance(expected, str) or not _SHA256_RE.fullmatch(expected):
                errors.append(f"invalid SHA-256 digest for artifact: {raw_relative}")
                continue
            actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
            checked_artifacts += 1
            seen_artifacts.add(relative.as_posix())
            if actual != expected:
                errors.append(f"artifact hash mismatch: {raw_relative}")
        missing_required = sorted(_REQUIRED_REPORT_ARTIFACTS - seen_artifacts)
        if missing_required:
            errors.append("required artifacts are not hashed: " + ", ".join(missing_required))

    def rows_from(payload: dict[str, Any] | None, field: str, label: str) -> list[dict[str, Any]]:
        if payload is None:
            return []
        raw = payload.get(field, [])
        if not isinstance(raw, list) or not all(isinstance(row, dict) for row in raw):
            errors.append(f"{label} {field} must be a list of objects")
            return []
        return [row for row in raw if isinstance(row, dict)]

    run_rows = rows_from(run_manifest, "topics", "run manifest")
    verification_rows = rows_from(verification_manifest, "results", "verification manifest")

    def row_ids(rows: list[dict[str, Any]], label: str) -> list[str]:
        ids: list[str] = []
        for row in rows:
            topic_id = row.get("topic_id")
            if not isinstance(topic_id, str) or not topic_id:
                errors.append(f"{label} contains a row without a topic_id")
                continue
            ids.append(topic_id)
        if len(set(ids)) != len(ids):
            errors.append(f"{label} contains duplicate topic_id values")
        return ids

    summary_ids = row_ids(summary_rows, "summary topics")
    run_ids = row_ids(run_rows, "run manifest topics")
    verification_ids = row_ids(verification_rows, "verification manifest results")
    if run_ids != summary_ids:
        errors.append("summary and run manifest topic rows disagree")

    def row_bool(row: dict[str, Any], names: tuple[str, ...], label: str) -> bool:
        key = next((name for name in names if name in row), names[0])
        value = row.get(key)
        if not isinstance(value, bool):
            errors.append(f"{label} {key} must be a boolean")
            return False
        return value

    summary_flags = [
        (
            row_bool(row, ("success",), f"summary topic {row.get('topic_id', '')}"),
            row_bool(row, ("lean_compiles", "compiles"), f"summary topic {row.get('topic_id', '')}"),
            row_bool(row, ("lean_has_sorry", "has_sorry"), f"summary topic {row.get('topic_id', '')}"),
        )
        for row in summary_rows
    ]
    verification_flags = [
        (
            row_bool(row, ("compiles",), f"verification topic {row.get('topic_id', '')}"),
            row_bool(row, ("lean_has_sorry",), f"verification topic {row.get('topic_id', '')}"),
        )
        for row in verification_rows
    ]

    if run_manifest is not None:
        if run_manifest.get("run_id") != root.name:
            errors.append("run manifest run_id does not match the report directory")
        if run_manifest.get("mode") != mode:
            errors.append("summary and run manifest mode disagree")
        if run_manifest.get("complete") != complete:
            errors.append("summary and run manifest complete flags disagree")
        if run_manifest.get("catalogue_topics") != selected_topics:
            errors.append("summary and run manifest selected-topic counts disagree")
        if run_manifest.get("verified_topics") != verified_topics:
            errors.append("summary and run manifest verified-topic counts disagree")
        for digest_name in ("source_digest", "config_digest"):
            if run_manifest.get(digest_name) != (summary or {}).get(digest_name):
                errors.append(f"summary and run manifest {digest_name} values disagree")
        if run_manifest.get("toolchain") != (summary or {}).get("toolchain"):
            errors.append("summary and run manifest toolchain values disagree")

    expected_row_count = len(summary_rows) if mode == "full" else 0
    if mode == "full" and len(summary_rows) != selected_topics:
        errors.append("full-mode summary topic rows do not match selected-topic count")
    if mode == "catalogue" and summary_rows:
        errors.append("catalogue-mode summary must not contain verification topic rows")
    if len(run_rows) != expected_row_count:
        errors.append("run manifest topic rows do not match the mode contract")
    if verification_ids != summary_ids[:expected_row_count]:
        errors.append("verification manifest topic rows do not match summary topics")

    if verification_manifest is not None:
        expected_true = sum(compiles for compiles, _ in verification_flags)
        expected_false = len(verification_rows) - expected_true
        if verification_manifest.get("verify_lean_ran") != bool(verification_rows):
            errors.append("verification manifest verify_lean_ran disagrees with its rows")
        if verification_manifest.get("topics_with_result") != len(verification_rows):
            errors.append("verification manifest topics_with_result disagrees with its rows")
        if verification_manifest.get("compiles_true") != expected_true:
            errors.append("verification manifest compiles_true disagrees with its rows")
        if verification_manifest.get("compiles_false") != expected_false:
            errors.append("verification manifest compiles_false disagrees with its rows")
        for summary_row, summary_flags_row, verification_flags_row in zip(
            summary_rows,
            summary_flags,
            verification_flags,
            strict=False,
        ):
            expected_compiles = summary_flags_row[1]
            expected_sorry = summary_flags_row[2]
            verification_compiles, verification_sorry = verification_flags_row
            if verification_compiles != expected_compiles:
                errors.append(f"verification compile flag disagrees for {summary_row.get('topic_id', '')}")
            if verification_sorry != expected_sorry:
                errors.append(f"verification sorry flag disagrees for {summary_row.get('topic_id', '')}")

    expected_verified = sum(
        success and compiles and not has_sorry
        for success, compiles, has_sorry in summary_flags
    )
    if verified_topics != expected_verified:
        errors.append("summary verified_topics disagrees with clean topic rows")
    if mode == "catalogue" and verified_topics != 0:
        errors.append("catalogue mode cannot report verified topics")

    if mode == "full" and complete:
        if summary is not None and summary.get("status") != "ok":
            errors.append("complete full-mode summary must have status ok")
        if not summary_rows or selected_topics == 0:
            errors.append("complete full-mode receipt must select at least one topic")
        if verified_topics != selected_topics:
            errors.append("complete full-mode receipt does not verify every selected topic")
        if any(row.get("verification_source") != "hermes_refined" for row in summary_rows):
            errors.append("complete full-mode rows must identify hermes_refined verification")
        if run_manifest is not None and run_manifest.get("verification_source") != "hermes_refined":
            errors.append("complete full-mode run manifest has the wrong verification source")
        if run_manifest is not None and run_manifest.get("lean_clean") is not True:
            errors.append("complete full-mode run manifest must mark lean_clean true")
    elif run_manifest is not None and run_manifest.get("verification_source") != "none" and not summary_rows:
        errors.append("run manifest reports a verification source without topic rows")

    claim_ready = (
        not errors
        and mode == "full"
        and complete
        and selected_topics > 0
        and selected_topics == verified_topics == len(summary_rows) == len(verification_rows)
    )
    if require_complete and not claim_ready:
        errors.append("complete full-mode receipt is required")

    return {
        "status": "ok" if not errors else "error",
        "valid": not errors,
        "claim_ready": claim_ready,
        "require_complete": require_complete,
        "report_root": str(root),
        "mode": mode,
        "complete": complete,
        "selected_topics": selected_topics,
        "verified_topics": verified_topics,
        "checked_artifacts": checked_artifacts,
        "errors": errors,
    }


@dataclass(frozen=True)
class ReportPaths:
    root: Path
    index_md: Path
    summary_json: Path
    hermes_md: Path
    lean_md: Path
    validation_md: Path
    manifest_json: Path
    run_manifest_json: Path | None = None

    def as_dict(self) -> dict[str, str]:
        data = {"root": str(self.root), "index_md": str(self.index_md), "summary_json": str(self.summary_json), "hermes_md": str(self.hermes_md), "lean_md": str(self.lean_md), "validation_md": str(self.validation_md), "verification_manifest": str(self.manifest_json)}
        if self.run_manifest_json is not None:
            data["run_manifest"] = str(self.run_manifest_json)
        return data


class Reporter:
    def __init__(self, project_root: Path, *, run_id: str | None = None, output_root: Path | None = None) -> None:
        self.project_root = Path(project_root)
        self.output_root = Path(output_root) if output_root is not None else self.project_root / "output"
        self.reports_dir = self.output_root / "reports"
        self.run_id = run_id or f"run_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

    @staticmethod
    def build_verification_manifest(results: Iterable[Any]) -> dict[str, Any]:
        rows = []
        for result in results:
            row = dict(result) if isinstance(result, dict) else {"topic_id": getattr(result, "topic_id", "")}
            if "compiles" not in row:
                row["compiles"] = bool(row.get("lean_compiles", getattr(result, "compiles", False)))
            if "lean_has_sorry" not in row:
                row["lean_has_sorry"] = bool(row.get("has_sorry", getattr(result, "has_sorry", False)))
            rows.append(row)
        return {"verify_lean_ran": bool(rows), "topics_with_result": len(rows), "compiles_true": sum(bool(r.get("compiles")) for r in rows), "compiles_false": sum(not bool(r.get("compiles")) for r in rows), "results": rows}

    def generate(self, catalogue: FEPTopicCatalogue, result: Any) -> ReportPaths:
        root = self.reports_dir / self.run_id
        root.mkdir(parents=True, exist_ok=True)
        topics = self._topic_rows(result)
        summary = result.as_dict() if hasattr(result, "as_dict") else dict(result)
        summary["topics"] = topics
        summary["catalogue"] = catalogue.summary()
        source_digest = _repository_digest(
            self.project_root,
            ("src", "scripts"),
            ("lean/FepSketches/fep_all.lean",),
        )
        config_digest = _repository_digest(
            self.project_root,
            (),
            ("config/settings.yaml", "config/topics.yaml", "manuscript/config.yaml", "lean/lean-toolchain", "lean/lakefile.lean"),
        )
        toolchain = {
            "lean_toolchain": (self.project_root / "lean" / "lean-toolchain").read_text(encoding="utf-8").strip()
            if (self.project_root / "lean" / "lean-toolchain").is_file() else "",
            "mathlib_tag": "",
        }
        lakefile = self.project_root / "lean" / "lakefile.lean"
        if lakefile.is_file():
            import re
            match = re.search(r'@\s*"([^"]+)"', lakefile.read_text(encoding="utf-8"))
            if match:
                toolchain["mathlib_tag"] = match.group(1)
        run_manifest = {
            "run_id": self.run_id,
            "mode": summary.get("mode", ""),
            "complete": bool(summary.get("complete", False)),
            "catalogue_topics": int(summary.get("catalogue_topics", len(catalogue.topics))),
            "verified_topics": int(summary.get("verified_topics", 0)),
            "capabilities": summary.get("capabilities", {}),
            "verification_source": "hermes_refined" if any(
                row.get("verification_source") == "hermes_refined" or row.get("hermes_success")
                for row in topics
            ) else "none",
            "lean_clean": bool(summary.get("complete", False))
            and int(summary.get("verified_topics", 0))
            == int(summary.get("catalogue_topics", len(catalogue.topics)))
            and summary.get("mode") == "full",
            "failure_reason": summary.get("failure_reason", ""),
            "source_digest": source_digest,
            "config_digest": config_digest,
            "toolchain": toolchain,
            "topics": topics,
        }
        summary["source_digest"] = source_digest
        summary["config_digest"] = config_digest
        summary["toolchain"] = toolchain
        summary["artifact_hashes"] = {}
        for name, content in (("hermes.md", self._hermes_md(topics)), ("lean.md", self._lean_md(getattr(result, "lean_stats", {}))), ("validation.md", self._validation_md(result)), ("index.md", self._index_md(catalogue, result))):
            _atomic_text(root / name, content)
        for row in topics:
            topic_id = str(row.get("topic_id", "")).strip()
            if topic_id:
                _atomic_text(root / "topics" / f"{topic_id}.md", self._topic_md(row))
        _atomic_text(root / "summary.json", json.dumps(summary, indent=2, sort_keys=True, default=str) + "\n")
        manifest = self.build_verification_manifest(topics)
        _atomic_text(root / "verification_manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        _atomic_text(root / "run_manifest.json", json.dumps(run_manifest, indent=2, sort_keys=True, default=str) + "\n")
        # ``summary.json`` contains this map, so hashing it would create a
        # self-referential value.  Hash every other report artifact, including
        # nested per-topic files, and make the exclusion explicit in the key
        # name's surrounding schema rather than publishing a stale digest.
        hashes = {
            p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*"))
            if p.is_file() and p.name != "summary.json"
        }
        summary["artifact_hashes"] = hashes
        _atomic_text(root / "summary.json", json.dumps(summary, indent=2, sort_keys=True, default=str) + "\n")
        return ReportPaths(root, root / "index.md", root / "summary.json", root / "hermes.md", root / "lean.md", root / "validation.md", root / "verification_manifest.json", root / "run_manifest.json")

    @staticmethod
    def _topic_rows(result: Any) -> list[dict[str, Any]]:
        direct = getattr(result, "topic_results", [])
        rows = [row.as_dict() if hasattr(row, "as_dict") else dict(row) for row in direct]
        if rows:
            return rows
        for stage in getattr(result, "stages", []):
            if stage.name != "Gauss Sessions" or not isinstance(stage.payload, dict):
                continue
            candidate = stage.payload.get("topics") or stage.payload.get("results") or []
            return [row.as_dict() if hasattr(row, "as_dict") else dict(row) for row in candidate]
        return []

    def _index_md(self, catalogue: FEPTopicCatalogue, result: Any) -> str:
        stats = getattr(result, "stats", {})
        rows = self._topic_rows(result)
        direct = sum(bool(row.get("hermes_lean_compiles")) for row in rows)
        final = sum(bool(row.get("lean_compiles")) and not bool(row.get("lean_has_sorry")) for row in rows)
        selected_topics = int(getattr(result, "catalogue_topics", 0) or len(rows) or len(catalogue.topics))
        lines = [f"# fep_lean run `{self.run_id}`", "", f"**Status:** `{getattr(result, 'status', 'unknown')}`", f"**Mode:** `{getattr(result, 'mode', 'full')}`", f"**Total Topics:** {selected_topics}", f"**Catalogue Topics:** {len(catalogue.topics)}", f"**Verified topics:** {getattr(result, 'verified_topics', 0)}", f"**Hermes-refined Lean compiled directly:** {direct}/{len(rows) or 0}", f"**Final Lean compiled:** {final}/{len(rows) or 0}", "", "## Stages", "", "| Stage | Status | Duration |", "| --- | --- | ---: |"]
        for stage in getattr(result, "stages", []):
            lines.append(f"| {stage.name} | {stage.status} | {stage.duration_s:.2f}s |")
        lines.extend(["", "## Metrics", "", "```json", json.dumps(stats, indent=2, default=str), "```", ""])
        return "\n".join(lines)

    def _hermes_md(self, topics: list[dict[str, Any]]) -> str:
        tokens = [int(row.get("tokens_used", 0) or 0) for row in topics if int(row.get("tokens_used", 0) or 0) > 0]
        models = sorted({str(row.get("hermes_model", "")) for row in topics if row.get("hermes_model")})
        direct = sum(bool(row.get("hermes_lean_compiles")) for row in topics)
        lines = [
            "# Hermes results", "",
            f"Processed: {len(topics)}",
            f"Successful: {sum(bool(t.get('hermes_success')) for t in topics)}",
            f"Cache hits: {sum(bool(t.get('cache_hit')) for t in topics)}/{len(topics) or 0}",
            f"Mean tokens/topic: {sum(tokens) // len(tokens) if tokens else 0}",
            f"Models used: {', '.join(models) or 'none'}",
            f"Hermes-refined Lean compiled: {direct}/{len(topics) or 0}", "",
        ]
        for row in topics:
            lines.extend([
                f"## {row.get('topic_id', '')}", "",
                f"- Hermes success: `{row.get('hermes_success', False)}`",
                f"- Model: `{row.get('hermes_model', '')}`",
                f"- Verification source: `{row.get('verification_source', 'none')}`",
                f"- Error: {row.get('error', '') or 'none'}",
                "",
                "### Explanation",
                "",
                str(row.get("explanation", "") or "(none)"),
                "",
                "### Refined Lean source",
                "",
                "```lean",
                str(row.get("refined_lean_sketch", "") or ""),
                "```",
                "",
            ])
        return "\n".join(lines)

    def _topic_md(self, row: dict[str, Any]) -> str:
        return "\n".join([
            f"# Topic {row.get('topic_id', '')}", "",
            "## Hermes Validation", "",
            f"- Success: `{row.get('hermes_success', False)}`",
            f"- Cache hit: `{row.get('cache_hit', False)}`",
            f"- Model: `{row.get('hermes_model', '') or 'none'}`",
            f"- Hermes-refined Lean compiled: `{row.get('hermes_lean_compiles', False)}`",
            f"- Final verification source: `{row.get('verification_source', 'none')}`",
            f"- Final Lean compiled cleanly: `{bool(row.get('lean_compiles')) and not bool(row.get('lean_has_sorry'))}`",
            f"- Error: {row.get('error', '') or 'none'}", "",
            "## Explanation", "", str(row.get("explanation", "") or "(no explanation recorded)"), "",
            "## Refined Lean source", "", "```lean", str(row.get("refined_lean_sketch", "") or ""), "```", "",
        ])

    def _lean_md(self, stats: dict[str, Any]) -> str:
        return "# Lean results\n\n```json\n" + json.dumps(stats, indent=2, default=str) + "\n```\n"

    def _validation_md(self, result: Any) -> str:
        payload: Any = next((s.payload for s in getattr(result, "stages", []) if s.name == "Environment Validation"), {})
        validation: dict[str, Any] = payload if isinstance(payload, dict) else {}
        lines = ["# Environment validation", "", f"Status: `{validation.get('status', 'not-run')}`", ""]
        for check in validation.get("checks", []):
            lines.append(f"- `{check.get('name', '')}`: `{check.get('ok', False)}` — {check.get('message', '')}")
        return "\n".join(lines) + "\n"
