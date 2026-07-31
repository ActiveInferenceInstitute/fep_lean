"""Build display-math LaTeX for each ``theorem`` in catalogue sketches (full-signature form).

``catalogue_sketches`` calls :func:`build_theorem_latex_from_sketches` at module load. Each
string is a single display block: ``amsmath`` ``aligned`` with, in order:

1. **Namespace ``variable``** line(s) in the sketch (e.g. ``{α : Type*} [MeasurableSpace α]``),
   when present, as the first row(s) of the block.
2. **Theorem binders** (parameters and explicit hypotheses) as the next row.
3. **Conclusion** (the type after the final top-level goal colon) as the last row.

The Lean statement (before ``:=``) is parsed; proof terms, ``by``, and ``tactic`` blocks are
omitted. Symbol mapping (μ→\\mu, etc.) is heuristic; goal is the standard mathematical reading
of the sketch, not a Lean pretty-printer. The bare type name ``Measure`` is emitted with a regex
so ``\\mathsf{IsProbabilityMeasure}`` and the prefix of ``MeasureTheory`` are not rewritten
again.
"""

from __future__ import annotations

import re


def _extract_variable_block(body: str) -> str:
    lines = body.splitlines()
    acc: list[str] = []
    for ln in lines:
        t = ln.strip()
        if t.startswith("variable "):
            acc.append(t[len("variable ") :].strip())
        elif acc and (t.startswith(("open ", "import ", "namespace ", "/-"))):
            break
    return " ".join(acc) if acc else ""


def _extract_theorem_stmt(body: str, name: str) -> str | None:
    """Return the Lean type (binders and conclusion) before the proof `:=` line or suffix.

    We cannot use a bare ``:=``+whitespace after the theorem name: the goal can contain
    ``t :=`` as substrings (e.g. ``+ μ t :=``), which would truncate the type.
    The proof always begins at the *last* top-level `` := `` that ends a line
    (optionally with ``by``/term after ``:=``).
    """
    m = re.search(r"(?m)^\s*theorem\s+" + re.escape(name) + r"\b", body)
    if not m:
        return None
    rest = body[m.end() :]
    acc: list[str] = []
    for line in rest.splitlines():
        t = line.rstrip()
        if re.search(r":=\s*", t):
            t2 = re.sub(r":=\s*.*$", "", t)
            t2 = t2.rstrip()
            if t2:
                acc.append(t2)
            return "\n".join(acc).strip() if acc else t2
        acc.append(line)
    return None


def _split_binders_and_goal(stmt: str) -> tuple[str, str]:
    stmt = stmt.strip()
    paren = brace = brack = 0
    last_ok = -1
    for i, ch in enumerate(stmt):
        if ch == "(":
            paren += 1
        elif ch == ")":
            paren = max(0, paren - 1)
        elif ch == "{":
            brace += 1
        elif ch == "}":
            brace = max(0, brace - 1)
        elif ch == "[":
            brack += 1
        elif ch == "]":
            brack = max(0, brack - 1)
        if paren == 0 and brace == 0 and brack == 0 and ch == ":":
            j = i - 1
            while j >= 0 and stmt[j] in " \t\n":
                j -= 1
            if j >= 0 and stmt[j] in ")]}":
                last_ok = i
    if last_ok < 0:
        m0 = re.match(r"^\s*:\s*(.+)$", stmt, re.DOTALL)
        if m0:
            return "", m0.group(1).strip()
        return stmt, ""
    return stmt[:last_ok].strip(), stmt[last_ok + 1 :].strip()


def _theorem_names_in_order(body: str) -> list[str]:
    return re.findall(r"^\s*theorem\s+([a-zA-Z0-9_]+)\s*", body, re.MULTILINE)


def _convert_lean_expr(s: str) -> str:
    t = s.strip()
    t = t.replace("μ", r"\mu")
    t = t.replace("α", r"\alpha")
    t = t.replace("β", r"\beta")
    t = t.replace("π", r"\pi")
    t = t.replace("σ", r"\sigma")
    t = t.replace("η", r"\eta")
    t = t.replace("γ", r"\gamma")
    t = t.replace("θ", r"\theta")
    t = t.replace("ω", r"\omega")
    t = t.replace("κ", r"\kappa")
    t = t.replace("λ", r"\lambda")
    t = t.replace("∅", r"\varnothing")
    t = t.replace("∪", r"\cup")
    t = t.replace("∩", r"\cap")
    t = t.replace("⊆", r"\subseteq")
    t = t.replace("⊂", r"\subset")
    t = t.replace("∈", r"\in")
    t = t.replace("∉", r"\notin")
    t = t.replace("≤", r"\le")
    t = t.replace("≥", r"\ge")
    t = t.replace("≠", r"\ne")
    t = t.replace("→", r"\Rightarrow")
    t = t.replace("↦", r"\mapsto")
    t = t.replace("∀", r"\forall")
    t = t.replace("∃", r"\exists")
    t = t.replace("∧", r"\wedge")
    t = t.replace("∨", r"\vee")
    t = t.replace("¬", r"\neg")
    t = t.replace("⊤", r"\top")
    t = t.replace("⊥", r"\bot")
    t = t.replace("⁻¹", r"^{-1}")
    t = t.replace("ᶜ", r"^{\mathrm{c}}")
    t = t.replace("∑", r"\sum")
    t = t.replace("∏", r"\prod")
    t = t.replace("×", r"\times")
    t = t.replace("·", r"\cdot")
    t = t.replace("∘", r"\circ")
    t = t.replace("↔", r"\leftrightarrow")
    t = t.replace("⇒", r"\Rightarrow")
    t = t.replace("↪", r"\hookrightarrow")
    t = t.replace("ℝ", r"\mathbb{R}")
    t = t.replace("ℕ", r"\mathbb{N}")
    t = t.replace(" ℤ ", r" \mathbb{Z} ")
    t = t.replace("ℚ", r"\mathbb{Q}")
    t = t.replace("⬝", r"\;")
    t = t.replace("₀", r"_{0}")
    t = t.replace("₁", r"_{1}")
    t = t.replace("₂", r"_{2}")
    t = t.replace("₃", r"_{3}")
    t = t.replace("₄", r"_{4}")
    t = t.replace("₅", r"_{5}")
    t = t.replace("fun", r"\lambda")
    t = t.replace("∂", r"\partial")
    t = t.replace("Type*", r"\mathsf{Type}^\*")
    t = t.replace("Type u", r"\mathsf{Type}~u")
    t = t.replace("Type v", r"\mathsf{Type}~v")
    t = t.replace("MeasureTheory", r"\mathsf{MeasureTheory}")
    t = t.replace("IsProbabilityMeasure", r"\mathsf{IsProbabilityMeasure}")
    t = t.replace("MeasurableSet", r"\mathsf{MeasurableSet}")
    t = t.replace("MeasurableSpace", r"\mathsf{MeasurableSpace}")
    t = t.replace("Enumerable", r"\mathsf{Enumerable}")
    t = re.sub(
        r"Measurable(?!Set|Space|Theory)",
        r"\\mathsf{Measurable}",
        t,
    )
    t = t.replace("ENNReal", r"\mathsf{ENNReal}")
    t = t.replace("Finset", r"\mathsf{Finset}")
    t = t.replace("List.nil", r"[\,]")
    t = t.replace("List", r"\mathsf{List}")
    t = t.replace("Set.univ", r"\Omega")
    t = t.replace("Set.", r"\mathsf{Set}.")
    t = t.replace("Set ", r"\mathsf{Set}~")
    # Do not use ``.replace("Measure", ...)`` — it rewrites the tail of
    # ``\mathsf{IsProbabilityMeasure}`` and the prefix of ``\mathsf{MeasureTheory}``.
    t = re.sub(
        r"(?<![A-Za-z])Measure(?!T)",
        r"\\mathsf{Measure}",
        t,
    )
    t = t.replace("OrderDual", r"\mathsf{OrderDual}")
    t = t.replace("Disjoint", r"\mathsf{Disjoint}")
    t = t.replace("Monotone", r"\mathsf{Monotone}")
    t = t.replace("Equiv", r"\mathsf{Equiv}")
    t = t.replace("Prod.fst", r"\pi_1")
    t = t.replace("Prod.snd", r"\pi_2")
    t = t.replace("priorParams", r"\mathsf{priorParams}")
    t = t.replace("update", r"\mathsf{update}")
    t = t.replace("foldl", r"\mathsf{foldl}")
    t = t.replace("assign", r"\mathsf{assign}")
    t = t.replace("Bool", r"\mathsf{Bool}")
    t = t.replace("Unit", r"\mathsf{Unit}")
    t = t.replace("Real", r"\mathbb{R}")
    t = t.replace("Nat", r"\mathbb{N}")
    t = t.replace("f∘g", r"f\circ g")
    t = t.replace("T⁻¹", r"T^{-1}")
    t = t.replace("f⁻¹", r"f^{-1}")
    t = t.replace("π_A", r"\pi_A")
    t = t.replace("π_1", r"\pi_1")
    t = t.replace("π_2", r"\pi_2")
    t = re.sub(r"(?<![A-Za-z])id(?![A-Za-z])", r"\\mathsf{id}", t)
    t = re.sub(r"(?<![A-Za-z])log(?![A-Za-z])", r"\\log", t, flags=re.IGNORECASE)
    t = re.sub(r"(?<![A-Za-z])ln(?![A-Za-z])", r"\\ln", t, flags=re.IGNORECASE)
    t = re.sub(r"(?<![A-Za-z])exp(?![A-Za-z])", r"\\exp", t, flags=re.IGNORECASE)
    t = t.replace(
        r"\mathsf{MeasurableSpace} \alpha", r"\mathsf{MeasurableSpace}~\alpha"
    )
    t = t.replace(r"\mathsf{Measure} \alpha", r"\mathsf{Measure}~\alpha")
    t = t.replace(
        r"\mathsf{IsProbabilityMeasure} \mu", r"\mathsf{IsProbabilityMeasure}~\mu"
    )
    t = re.sub(r"\\mu\s+\\varnothing", r"\\mu(\\varnothing)", t)
    t = re.sub(r"\\mu\s+\\Omega\b", r"\\mu(\\Omega)", t)
    return t


def _wrap_aligned(rows: list[str]) -> str:
    if not rows:
        return r"\mathsf{?}"
    if len(rows) == 1:
        return rows[0]
    lines = [f"&{r}" for r in rows if r.strip()]
    return r"\begin{aligned}" + "\n" + " \\\\\n".join(lines) + "\n" + r"\end{aligned}"


def _one_theorem_latex(var_ctx: str, binders: str, goal: str, *, with_ctx: bool) -> str:
    conv_var = _convert_lean_expr(var_ctx) if var_ctx else ""
    conv_b = _convert_lean_expr(binders) if binders else ""
    conv_g = _convert_lean_expr(goal) if goal else ""
    rows: list[str] = []
    if with_ctx and conv_var:
        rows.append(conv_var)
    if conv_b:
        rows.append(conv_b)
    if conv_g:
        rows.append(conv_g)
    if not rows:
        return r"\mathsf{?}"
    if len(rows) == 1:
        return _wrap_aligned(rows)
    return _wrap_aligned(rows)


def build_theorem_latex_from_sketches(sketches: dict[str, str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for body in sketches.values():
        vblock = _extract_variable_block(body)
        names = _theorem_names_in_order(body)
        for name in names:
            stmt = _extract_theorem_stmt(body, name)
            if not stmt:
                out[name] = r"\mathsf{?}"
                continue
            b, g = _split_binders_and_goal(stmt)
            out[name] = _one_theorem_latex(vblock, b, g, with_ctx=bool(vblock.strip()))
    return out


__all__ = ["build_theorem_latex_from_sketches"]
