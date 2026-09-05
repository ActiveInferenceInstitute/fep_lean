#!/usr/bin/env python3
"""Q5 asymmetric axis-sensitive normalized dyadic control fixture.

Hand-authored in the identical assignment shape as the accepted P1 pymdp
render output (five table literals assigned once, straight-line, inside
``main()``). All values are dyadic (denominator a power of two), every
column is stochastic under the frozen pymdp layout, and the tables are
deliberately asymmetric so that axis transposition breaks normalization:

- ``A`` rows differ per outcome and the matrix is not symmetric under
  transposition (``A[0][0] = 1/4`` while ``A[1][0] = 3/4``);
- ``B`` slices are column-stochastic only (rows are next states), so
  swapping the next/previous axes yields non-stochastic columns;
- ``E`` is a third distinct dyadic vector (``3/8, 5/8``).

This fixture is sibling-independent: it never touches the GNN pipeline.
"""
from __future__ import annotations


def main() -> int:
    """Table literals only; nothing here is executed by the Q5 extractor."""
    # Matrices embedded verbatim in the accepted render-output shape.
    A_data = [[0.25, 0.5], [0.75, 0.5]]
    B_data = [
        [[0.25, 0.5], [0.75, 0.125]],
        [[0.75, 0.5], [0.25, 0.875]],
    ]
    C_data = [0.25, 0.75]
    D_data = [0.5, 0.5]
    E_data = [0.375, 0.625]
    # Single consumer keeps the fixture lint-clean without altering the shape.
    tables = {"A": A_data, "B": B_data, "C": C_data, "D": D_data, "E": E_data}
    return len(tables) % 5


if __name__ == "__main__":
    raise SystemExit(main())
