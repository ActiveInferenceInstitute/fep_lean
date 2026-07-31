"""Transactional Markdown and JSON run reports."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from catalogue.topics import FEPTopicCatalogue


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
