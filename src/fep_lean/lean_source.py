"""Conservative Lean source-text normalization for structural validators."""

from __future__ import annotations

import re


def lean_code_without_comments(source: str) -> str:
    """Blank nested comments and strings while preserving source offsets.

    Lean permits nested block comments.  Regex-based structural checks must not
    accept declarations or dependencies that occur only in comments or string
    literals, while source-block extraction still needs exact byte offsets.
    Every removed non-newline character is therefore replaced with one space.
    """
    output: list[str] = []
    index = 0
    block_depth = 0
    in_line_comment = False
    in_string = False
    escaped = False
    while index < len(source):
        current = source[index]
        following = source[index : index + 2]
        if in_line_comment:
            if current == "\n":
                in_line_comment = False
                output.append(current)
            else:
                output.append(" ")
            index += 1
            continue
        if block_depth:
            if following == "/-":
                block_depth += 1
                output.extend((" ", " "))
                index += 2
                continue
            if following == "-/":
                block_depth -= 1
                output.extend((" ", " "))
                index += 2
                continue
            output.append(current if current == "\n" else " ")
            index += 1
            continue
        if in_string:
            output.append(current if current == "\n" else " ")
            if escaped:
                escaped = False
            elif current == "\\":
                escaped = True
            elif current == '"':
                in_string = False
            index += 1
            continue
        if following == "--":
            in_line_comment = True
            output.extend((" ", " "))
            index += 2
            continue
        if following == "/-":
            block_depth = 1
            output.extend((" ", " "))
            index += 2
            continue
        if current == '"':
            in_string = True
            output.append(" ")
            index += 1
            continue
        output.append(current)
        index += 1
    return "".join(output)


def lean_declaration_conclusion(source: str) -> str:
    """Return a theorem/lemma result after its final top-level header colon."""
    code = lean_code_without_comments(source)
    proof_start = re.search(r":=\s*by\b", code)
    if proof_start is None:
        raise ValueError("Lean declaration has no `:= by` proof boundary")
    header = code[: proof_start.start()]
    paren = brace = bracket = 0
    conclusion_colon: int | None = None
    for index, character in enumerate(header):
        if character == "(":
            paren += 1
        elif character == ")":
            paren = max(0, paren - 1)
        elif character == "{":
            brace += 1
        elif character == "}":
            brace = max(0, brace - 1)
        elif character == "[":
            bracket += 1
        elif character == "]":
            bracket = max(0, bracket - 1)
        elif character == ":" and paren == brace == bracket == 0:
            conclusion_colon = index
    if conclusion_colon is None:
        raise ValueError("Lean declaration has no top-level conclusion colon")
    conclusion = header[conclusion_colon + 1 :].strip()
    if not conclusion:
        raise ValueError("Lean declaration conclusion is empty")
    return conclusion


__all__ = ["lean_code_without_comments", "lean_declaration_conclusion"]
