"""
snapbend/drawing/sections.py
----------------------------
Sezioni di lamiera in una tavola a viste letta da `topo.island()` (MAP.md D69).

topo dà i contorni chiusi (outer di ogni isola, i suoi inners, le curve
chiuse in `loose`) e dice solo la loro forma geometrica; qui si chiede a
`read_section()` (la "dima", il segnale triplo) se un contorno è una sezione
di lamiera: un profilo piegato (L, U, Z, omega, sella) disegnato in sezione è
un contorno chiuso con due tappi di spessore. Un contorno alla volta: i
profili chiusi (tubi) non sono di snapbend (D69).

I contorni che contengono spline/ellissi non si leggono: `read_section()`
conosce solo linee, archi e cerchi.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional, Union

import topo

from ..rules.read_section import SectionReading, SheetThicknessTable, read_section

ClosedContour = Union[topo.model.Contour, topo.model.ClosedCurve]


@dataclass
class DrawnSection:
    """Una sezione di lamiera trovata nella tavola.

    `contour`: il contorno letto (un outer, un inner o un `ClosedCurve` di
    `loose`); `cluster_ref`: indice in `result.clusters` dell'isola a cui
    appartiene (`None` fuori da ogni isola); `reading`: cosa ha letto
    `read_section()` — spessore, piegata o no, mezzeria.
    """
    contour: ClosedContour
    cluster_ref: Optional[int]
    reading: SectionReading


def find_sections(
    result: topo.Result,
    table: Optional[SheetThicknessTable] = None,
) -> List[DrawnSection]:
    """Tutti i contorni chiusi di `result` che `read_section()` dice lamiera
    (`is_sheet_metal`); se è anche piegata lo dice `reading.is_bent`."""
    table = table or SheetThicknessTable.load()
    found: List[DrawnSection] = []
    for contour, ref in _contours(result):
        reading = _read(contour, table)
        if reading is not None and reading.is_sheet_metal:
            found.append(DrawnSection(contour, ref, reading))
    return found


def _contours(result: topo.Result) -> List[tuple]:
    """(contorno, cluster_ref) per ogni outer, inner e curva chiusa in loose.
    Un loose con un ruolo non strutturale (cornice, cartiglio…) è stato
    tolto apposta dal chiamante: non si legge."""
    contours = []
    for i, cluster in enumerate(result.clusters):
        contours.append((cluster.outer, i))
        contours += [(inner, i) for inner in cluster.inners]
    contours += [
        (curve, curve.cluster_ref) for curve in result.loose
        if isinstance(curve, topo.model.ClosedCurve)
        and (curve.role == "unknown" or topo.is_structural_role(curve.role))
    ]
    return contours


def _read(contour: ClosedContour, table: SheetThicknessTable) -> Optional[SectionReading]:
    """`read_section()` sugli spigoli del contorno; `None` se ha spigoli che
    `read_section()` non conosce (spline, ellisse)."""
    entities = []
    for seg in contour.segments:
        entity = _entity(seg)
        if entity is None:
            return None
        entities.append(entity)
    return read_section(entities, table=table)


def _entity(seg) -> Optional[dict]:
    """Segmento nativo di topo -> entità dello schema di `read_section()`
    (angoli in gradi; topo li tiene in radianti)."""
    if isinstance(seg, topo.primitives.LineSeg):
        return {"type": "line", "start": seg.start, "end": seg.end}
    if isinstance(seg, topo.primitives.ArcSeg):
        return {"type": "arc", "center": seg.center, "radius": seg.radius,
                "start_angle": math.degrees(seg.start_angle),
                "end_angle": math.degrees(seg.end_angle), "ccw": seg.ccw}
    if isinstance(seg, topo.primitives.CircleSeg):
        return {"type": "circle", "center": seg.center, "radius": seg.radius}
    return None
