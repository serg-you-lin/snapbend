"""
snapbend/flat/trim.py
---------------------
Tratteggio delle linee di piega: la piega si disegna a tratti invece che
intera — un tratto attaccato a ogni capo, tratti centrali, vuoti uguali. La
geometria del tratteggio è di forge (`forge.geometry.dash_line`, forge MAP.md
D115); qui c'è il significato: quali linee, con che misure (MAP.md D63).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional, Union

from forge.core.geometry import dash_line
from forge.model import ForgeResult

from .model import BendingLine


@dataclass(frozen=True)
class DashPattern:
    """Misure del tratteggio di una piega: `head` sul primo capo, `tail`
    sull'ultimo, `n_middle` tratti lunghi `middle` in mezzo."""
    head:     float
    tail:     float
    middle:   float = 0.0
    n_middle: int   = 0


# Regola del chiamante: dalla piega alle sue misure; None = la piega resta intera.
DashRule = Callable[[BendingLine], Optional[DashPattern]]


def trim_bending_lines(result: ForgeResult,
                       pattern: Union[DashPattern, DashRule]) -> ForgeResult:
    """
    Tratteggia ogni `BendingLine` di `result` con `pattern`: le stesse misure
    per tutte, o una regola che le sceglie piega per piega (per esempio dalla
    lunghezza). Il tratteggio parte sempre dall'asse intero (`geometry`), quindi
    ripeterlo lo sostituisce, non lo somma. Una piega che i tratti coprono
    tutta, o per cui la regola dà None, resta intera (`dashes` vuoto).

    Muta `result` in-place (`BendingLine.dashes`) e lo ritorna.
    """
    rule = pattern if callable(pattern) else (lambda _bl: pattern)
    for cluster in result.clusters:
        for bl in cluster.features("bending_lines"):
            p = rule(bl)
            coords = list(bl.geometry.coords)
            dashes = [] if p is None else dash_line(coords[0], coords[-1], p.head, p.tail,
                                                    p.middle, p.n_middle)
            bl.dashes = dashes if len(dashes) > 1 else []
    return result
