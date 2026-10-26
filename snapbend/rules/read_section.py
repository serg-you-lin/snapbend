"""
snapbend/rules/read_section.py
------------------------------
Read a 2D section outline (lines + arcs, forge-neutral schema) and decide
whether it is bent sheet metal, then recover the parameters the flat-length
engine needs.

This is the first piece of the drawing interpreter. It is the inverse of
snapbend/model/section.py: `Section` builds a section from parameters, this reads
the parameters back from a section.

"Is it bent sheet metal?" - three signals:
  1. the faces are parallel at a constant distance  -> candidate thickness;
  2. that thickness exists in the sheet-thickness table (sheet_thicknesses.json);
  3. the rounded corners are concentric arc pairs whose radii differ by
     exactly that thickness  -> it is BENT (not a flat blank, not a cut
     outline).

Signal 3 also fires on a pair of full concentric circles (a tube's top
view, MAP.md D42), not just partial arcs - a circle entity is read as a
closed 360-degree loop.

The centerline is not read from the drawing: it is the midline between the
two faces. `centerline_segments` are apex-to-apex, `angles` follow the
naming scheme (flat = 180, bend up = 90, bend down = 270) - the same
inputs `BentProfile` / `Section` take. When the recovered profile has no
straight flange anywhere - a bare calandra arc, cap-arc-cap, e.g. a
rolled "sella" (MAP.md D42) - `centerline_segments`/`angles` are left
empty and the radius/angle come back instead in `pure_arc_radius`/
`pure_arc_angle_deg`: that shape is `Cylinder`/`Cone` territory, not
`BentProfile` (which requires real straight flanges on both sides of
every bend).

MAP.md D43 (retracted, 11 Sep 2026): this module briefly imported topo
(`topo.load_geometry` + its topology engine) to walk the outline instead
of the hand-rolled walker below. Reverted before `pippo` (the future
drawing interpreter this feeds, see `docs/ARCHITECTURE.md`) exists for
real: deciding the forge-native shape of this contract now, for an
imagined consumer, was exactly the mistake D43's phases 2-4 already made
once. This module is forge-free again, like the rest of `snapbend` minus
`io/dxf.py` - revisit when `pippo` is real and its actual needs are known.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple
from .officina import officina_file

_TOL = 1e-6
_SHEET_TABLE = Path(__file__).resolve().parent.parent / "data" / "sheet_thicknesses.json"

Point = Tuple[float, float]


# --------------------------------------------------------------------------
# sheet-thickness table
# --------------------------------------------------------------------------

@dataclass
class SheetThicknessTable:
    thicknesses_mm: List[float]
    tolerance_mm: float = 0.2

    @classmethod
    def load(cls, path: str | Path | None = None) -> "SheetThicknessTable":
        """Da `path`; altrimenti dalla cartella officina, poi dall'esempio generico del repo."""
        path = path or officina_file("sheet_thicknesses.json") or _SHEET_TABLE
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(
            thicknesses_mm=sorted(float(t) for t in data["thicknesses_mm"]),
            tolerance_mm=float(data.get("tolerance_mm", 0.2)),
        )

    def contains(self, thickness: float) -> bool:
        return any(abs(thickness - t) <= self.tolerance_mm
                   for t in self.thicknesses_mm)


# --------------------------------------------------------------------------
# result
# --------------------------------------------------------------------------

@dataclass
class SectionBend:
    """Una piega letta da sola, senza camminare il profilo (MAP.md D74): una
    coppia di archi concentrici i cui raggi differiscono dello spessore.

    angle:        gradi di rotazione da piatto (convenzione di `Bend.angle`) —
                  l'arco più lungo della coppia: l'altro può essere coperto
    inner_radius: il raggio minore della coppia
    center:       il centro comune
    """
    angle:        float
    inner_radius: float
    center:       Point


@dataclass
class SectionReading:
    is_sheet_metal: bool
    is_bent: bool
    thickness: Optional[float]
    centerline_segments: List[float] = field(default_factory=list)
    angles: List[float] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    # Bare calandra arc, no straight flange anywhere (MAP.md D42) - set
    # instead of centerline_segments/angles, which do not fit that shape.
    pure_arc_radius: Optional[float] = None
    pure_arc_angle_deg: Optional[float] = None
    # ogni piega che si legge da sola, anche quando il profilo non si
    # ricostruisce (MAP.md D74)
    bends: List[SectionBend] = field(default_factory=list)


# --------------------------------------------------------------------------
# geometry helpers
# --------------------------------------------------------------------------

def _dist(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _mid(a: Point, b: Point) -> Point:
    return ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)


def _arc_point(center: Point, radius: float, angle_deg: float) -> Point:
    a = math.radians(angle_deg)
    return (center[0] + radius * math.cos(a), center[1] + radius * math.sin(a))


def _sweep_deg(a0: float, a1: float, ccw: bool) -> float:
    """Signed sweep from a0 to a1 in (-360, 360), positive when ccw."""
    d = (a1 - a0) % 360.0
    if not ccw:
        d -= 360.0
    if d <= -360.0 + 1e-9:
        d += 360.0
    return d


class _Edge:
    __slots__ = ("kind", "start", "end", "center", "radius", "a0", "a1", "ccw", "length")

    def __init__(self, entity: dict):
        self.kind = entity["type"]
        if self.kind == "line":
            self.start = tuple(entity["start"])
            self.end = tuple(entity["end"])
            self.center = self.radius = self.a0 = self.a1 = self.ccw = None
            self.length = _dist(self.start, self.end)
        elif self.kind == "arc":
            self.center = tuple(entity["center"])
            self.radius = float(entity["radius"])
            self.a0 = float(entity["start_angle"])
            self.a1 = float(entity["end_angle"])
            self.ccw = bool(entity.get("ccw", True))
            self.start = _arc_point(self.center, self.radius, self.a0)
            self.end = _arc_point(self.center, self.radius, self.a1)
            self.length = abs(math.radians(_sweep_deg(self.a0, self.a1, self.ccw))) * self.radius
        elif self.kind == "circle":
            # Un giro chiuso, non un arco parziale: niente da camminare in
            # una catena (start ed end coincidono, non un capo/altro capo
            # distinti) - _sweep_deg(0, 360, ...) darebbe 0 per il modulo
            # 360, quindi la lunghezza si calcola diretta (2*pi*raggio),
            # non passando dalla stessa formula sweep-based dell'arco.
            self.center = tuple(entity["center"])
            self.radius = float(entity["radius"])
            self.a0, self.a1, self.ccw = 0.0, 360.0, True
            self.start = self.end = _arc_point(self.center, self.radius, 0.0)
            self.length = 2.0 * math.pi * self.radius
        else:
            raise ValueError(f"unsupported entity type: {self.kind!r}")

    def other(self, p: Point) -> Point:
        return self.end if _dist(p, self.start) < _dist(p, self.end) else self.start

    def touches(self, p: Point, tol: float) -> bool:
        return _dist(p, self.start) <= tol or _dist(p, self.end) <= tol


# --------------------------------------------------------------------------
# main entry point
# --------------------------------------------------------------------------

def read_section(
    entities: List[dict],
    table: Optional[SheetThicknessTable] = None,
    join_tol: float = 1e-4,
) -> SectionReading:
    edges = [_Edge(e) for e in entities if e.get("type") in ("line", "arc", "circle")]
    notes: List[str] = []
    # 2, not 3: a tube's top view is only 2 entities (two full concentric
    # circles, no straight cap at all) and is already a complete signal
    # (thickness + is_bent, MAP.md D42) - it must not be discarded here.
    if len(edges) < 2:
        return SectionReading(False, False, None,
                              notes=["too few edges for a section outline"])

    table = table or SheetThicknessTable.load()
    thickness, t_notes = _thickness(edges, table)
    notes += t_notes

    is_bent = thickness is not None and _has_concentric_pair(edges, thickness)

    is_sheet = thickness is not None and table.contains(thickness)
    if thickness is not None and not is_sheet:
        notes.append(f"thickness {thickness:.3f} not in sheet-thickness table")

    segments: List[float] = []
    angles: List[float] = []
    pure_arc_radius: Optional[float] = None
    pure_arc_angle: Optional[float] = None
    bends: List[SectionBend] = []
    if thickness is not None:
        bends = _bends(edges, thickness)
        try:
            segments, angles, pure_arc_radius, pure_arc_angle = _recover_centerline(
                edges, thickness, join_tol
            )
        except _RecoverError as exc:
            # Il contorno ha più della sezione (un moncherino non piegato
            # disegnato insieme, MAP.md D74): si prova a leggerla da una
            # faccia sola, quella che corre intera fra due tappi.
            try:
                segments, angles = _recover_from_one_face(edges, thickness, join_tol)
                # una piega letta dalla faccia col compagno nascosto (D75)
                is_bent = is_bent or bool(angles)
                notes.append(f"profile read from one face; the rest of the outline "
                             f"is not part of it ({exc})")
            except _RecoverError as one_face:
                notes.append(f"centerline not recovered: {exc}; one face: {one_face}")

    return SectionReading(
        is_sheet_metal=bool(is_sheet),
        is_bent=bool(is_bent),
        thickness=thickness,
        centerline_segments=segments,
        angles=angles,
        notes=notes,
        pure_arc_radius=pure_arc_radius,
        pure_arc_angle_deg=pure_arc_angle,
        bends=bends,
    )


# --------------------------------------------------------------------------
# signal 1 + 2: thickness from parallel faces / concentric arcs (or circles)
# --------------------------------------------------------------------------

def _thickness(edges: List[_Edge], table: SheetThicknessTable) -> Tuple[Optional[float], List[str]]:
    notes: List[str] = []

    arc_diffs: List[float] = []
    by_center: dict = {}
    for e in edges:
        if e.kind in ("arc", "circle"):
            key = (round(e.center[0], 4), round(e.center[1], 4))
            by_center.setdefault(key, []).append(e.radius)
    for radii in by_center.values():
        if len(radii) >= 2:
            arc_diffs.append(round(max(radii) - min(radii), 4))

    face_pairs = _face_pair_distances(edges)
    face_dists = [d for d, _ in face_pairs]

    if arc_diffs:
        thickness = _mode(arc_diffs)
        if any(abs(d - thickness) > 0.01 for d in arc_diffs):
            notes.append("bend radii do not all differ by the same amount")
        near_face = [d for d in face_dists if abs(d - thickness) < 0.05]
        if face_dists and not near_face:
            notes.append("arc pairs and face distances disagree on thickness")
        return thickness, notes

    if face_dists:
        # Pesata sul tratto in cui le facce si fronteggiano: le due facce di
        # una lamiera corrono per tutta la sua lunghezza, un tappo contro il
        # lato opposto solo per lo spessore. Senza peso, in un piatto 200x3 o
        # in una L a spigolo vivo, 3 e 200 (o 100) pareggiano.
        #
        # Un pezzo diverso fuso nello stesso contorno può fronteggiare la
        # lamiera più a lungo delle sue due facce (un blocco nell'angolo di
        # una L, MAP.md D75). Allora vince un candidato più leggero solo se è
        # uno spessore di tabella E la lamiera ha le sue due testate di
        # quella misura: un gradino di 3 in una vista di faccia non basta.
        counts = _weights(face_dists, [w for _, w in face_pairs])
        thickness = max(counts, key=counts.get)
        if not table.contains(thickness):
            sheets = {d: w for d, w in counts.items()
                      if table.contains(d) and _cap_count(edges, d) >= 2}
            if sheets:
                heavier = thickness
                thickness = max(sheets, key=sheets.get)
                notes.append(f"faces {heavier:.3f} apart face each other longer, but that "
                             f"is not a sheet thickness; {thickness:.3f} has its two end caps")
        if any(abs(d - thickness) > 0.05 for d in face_dists):
            notes.append("face distances not constant")
        return thickness, notes

    return None, ["no parallel faces or concentric arcs found"]


def _face_pair_distances(edges: List[_Edge]) -> List[Tuple[float, float]]:
    """(distance, overlap) for lines that genuinely face each other
    (parallel, apart, and overlapping along their shared direction)."""
    lines = [e for e in edges if e.kind == "line"]
    out: List[Tuple[float, float]] = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            a, b = lines[i], lines[j]
            delta = abs(_direction(a) - _direction(b)) % 180.0
            if min(delta, 180.0 - delta) > 0.5:
                continue
            d = _perp_distance(a, b)
            if d <= _TOL:
                continue
            overlap = _projection_overlap(a, b)
            if overlap < 0.5 * min(a.length, b.length):
                continue
            out.append((round(d, 4), overlap))
    return out


def _projection_overlap(a: _Edge, b: _Edge) -> float:
    dx, dy = a.end[0] - a.start[0], a.end[1] - a.start[1]
    n = math.hypot(dx, dy)
    if n < _TOL:
        return 0.0
    ux, uy = dx / n, dy / n

    def proj(p):
        return (p[0] - a.start[0]) * ux + (p[1] - a.start[1]) * uy

    a0, a1 = sorted((proj(a.start), proj(a.end)))
    b0, b1 = sorted((proj(b.start), proj(b.end)))
    return max(0.0, min(a1, b1) - max(a0, b0))


def _direction(line: _Edge) -> float:
    return math.degrees(math.atan2(line.end[1] - line.start[1],
                                   line.end[0] - line.start[0])) % 180.0


def _perp_distance(a: _Edge, b: _Edge) -> float:
    dx, dy = a.end[0] - a.start[0], a.end[1] - a.start[1]
    n = math.hypot(dx, dy)
    if n < _TOL:
        return 0.0
    return abs((b.start[0] - a.start[0]) * (-dy) + (b.start[1] - a.start[1]) * dx) / n


def _has_concentric_pair(edges: List[_Edge], thickness: float) -> bool:
    by_center: dict = {}
    for e in edges:
        if e.kind in ("arc", "circle"):
            key = (round(e.center[0], 4), round(e.center[1], 4))
            by_center.setdefault(key, []).append(e.radius)
    for radii in by_center.values():
        if len(radii) >= 2 and abs((max(radii) - min(radii)) - thickness) < 1e-3:
            return True
    return False


def _cap_count(edges: List[_Edge], thickness: float) -> int:
    """Quante rette lunghe esattamente `thickness`: le testate di una lamiera."""
    return sum(1 for e in edges if e.kind == "line" and abs(e.length - thickness) < 1e-3)


def _mode(values: List[float], weights: Optional[List[float]] = None) -> float:
    """Il valore più frequente (entro 1e-3); con `weights`, quello di peso totale maggiore."""
    counts = _weights(values, weights)
    return max(counts, key=counts.get)


def _weights(values: List[float], weights: Optional[List[float]] = None) -> dict:
    """valore -> peso totale (o conteggio), i valori entro 1e-3 contano come uno."""
    counts: dict = {}
    for v, w in zip(values, weights or [1.0] * len(values)):
        hit = next((k for k in counts if abs(k - v) < 1e-3), v)
        counts[hit] = counts.get(hit, 0) + w
    return counts


# --------------------------------------------------------------------------
# centerline recovery
# --------------------------------------------------------------------------

class _RecoverError(RuntimeError):
    pass


def _recover_centerline(
    edges: List[_Edge], thickness: float, tol: float,
):
    """
    Returns (segments, angles, pure_arc_radius, pure_arc_angle_deg) - the
    last two only set for a bare calandra arc (MAP.md D42, no straight
    flange anywhere), the first two then left empty (see module docstring).
    """
    caps = [e for e in edges if e.kind == "line" and abs(e.length - thickness) < 1e-3]
    if len(caps) != 2:
        raise _RecoverError(f"expected 2 end caps, found {len(caps)}")

    sides = _split_into_sides(edges, caps, tol)
    if len(sides) != 2:
        raise _RecoverError(f"expected 2 face chains, found {len(sides)}")

    # Le due facce si camminano dallo STESSO tappo: ognuna parte dal capo di
    # caps[0] che tocca. L'ordine delle entità in ingresso non conta (un
    # contorno di topo arriva come anello testa-coda, non come lo scrive Section).
    cap = caps[0]
    chain_a, chain_b = (
        _order_chain(side, cap.start if any(e.touches(cap.start, tol) for e in side) else cap.end, tol)
        for side in sides
    )
    if chain_a is None or chain_b is None or len(chain_a) != len(chain_b):
        raise _RecoverError("face chains do not correspond")

    # walk the two chains together -> centerline primitives
    cl_lines: List[float] = []          # straight length of each centerline segment
    cl_setbacks: List[float] = []       # setback contributed by each centerline arc
    cl_turns: List[float] = []          # signed sweep (deg) of each centerline arc
    cl_radii: List[float] = []          # centerline radius of each arc
    for k, (ea, eb) in enumerate(zip(chain_a, chain_b)):
        if ea.kind != eb.kind:
            raise _RecoverError("face chains out of step")
        if ea.kind == "line":
            if k > 0 and chain_a[k - 1].kind == "line":
                # due tratti dritti senza arco in mezzo: spigolo vivo, il
                # raggio di piega non è disegnato — non lo si inventa qui
                raise _RecoverError("sharp corner: no bend radius drawn")
            p0 =_mid(_chain_vertex(chain_a, k, tol), _chain_vertex(chain_b, k, tol))
            p1 = _mid(_chain_vertex(chain_a, k + 1, tol), _chain_vertex(chain_b, k + 1, tol))
            cl_lines.append(_dist(p0, p1))
        else:
            if _dist(ea.center, eb.center) > 1e-3:
                raise _RecoverError("arc pair not concentric")
            r_cl = (ea.radius + eb.radius) / 2.0
            sweep = _sweep_deg(ea.a0, ea.a1, ea.ccw)
            cl_turns.append(sweep)
            cl_radii.append(r_cl)
            cl_setbacks.append(r_cl * math.tan(math.radians(abs(sweep)) / 2.0))

    if not cl_lines and len(cl_turns) == 1:
        # Bare calandra arc (MAP.md D42): cap -> arc -> cap, no straight
        # flange anywhere. Not BentProfile's shape (it needs real straight
        # length on both sides of every bend) - Cylinder/Cone territory.
        return [], [], cl_radii[0], abs(cl_turns[0])

    segments, angles = _compose(cl_lines, cl_turns, cl_setbacks)
    return segments, angles, None, None


def _compose(cl_lines: List[float], cl_turns: List[float], cl_setbacks: List[float]):
    """Tratti dritti della mezzeria + archi -> segmenti apice-apice e angoli
    nello schema di naming, in orientamento canonico."""
    n = len(cl_lines)
    segments: List[float] = []
    for j in range(n):
        seg = cl_lines[j]
        if j >= 1:
            seg += cl_setbacks[j - 1]
        if j <= n - 2:
            seg += cl_setbacks[j]
        segments.append(round(seg, 4))

    angles = [round(180.0 - t, 4) for t in cl_turns]
    return _canonical(segments, angles)


def _partner(arc: _Edge, edges: List[_Edge], thickness: float) -> Optional[_Edge]:
    """L'arco concentrico ad `arc` il cui raggio differisce dello spessore."""
    for e in edges:
        if (e is not arc and e.kind == "arc" and _dist(e.center, arc.center) <= 1e-3
                and abs(abs(e.radius - arc.radius) - thickness) < 1e-3):
            return e
    return None


def _bends(edges: List[_Edge], thickness: float) -> List[SectionBend]:
    """Ogni coppia di archi concentrici a distanza `thickness` è una piega
    (MAP.md D74). L'angolo è lo sweep più lungo della coppia: un arco può
    essere coperto in parte (moncherino disegnato davanti), mai allungato."""
    out: List[SectionBend] = []
    used: set = set()
    for a in edges:
        if a.kind != "arc" or id(a) in used:
            continue
        b = _partner(a, edges, thickness)
        if b is None or id(b) in used:
            continue
        used.update((id(a), id(b)))
        sweep = max(abs(_sweep_deg(e.a0, e.a1, e.ccw)) for e in (a, b))
        out.append(SectionBend(angle=round(sweep, 4), inner_radius=min(a.radius, b.radius),
                               center=a.center))
    return out


def _recover_from_one_face(edges: List[_Edge], thickness: float, tol: float):
    """Mezzeria da UNA faccia (MAP.md D74), quando il contorno ha più della
    sezione — tipico: il moncherino non piegato dell'ala, disegnato nello
    stesso contorno, copre lo spigolo e aggiunge un terzo tappo.

    Una faccia vale se corre intera da un tappo all'altro, retta-arco-retta
    alternati, ogni arco tangente alle sue rette. La retta di una faccia è
    lunga quanto quella della mezzeria (i punti di tangenza stanno sullo
    stesso raggio); l'arco della mezzeria sta a t/2 dall'arco, verso la
    lamiera. Da che parte sta la lamiera lo dice il compagno concentrico, se
    c'è anche solo in parte; se è coperto del tutto (un altro pezzo fuso
    nell'angolo, MAP.md D75) lo dice il tappo da cui la faccia parte: va da
    questa faccia all'altra. Serve esattamente una faccia così: zero o due
    sono un'ambiguità, non si sceglie."""
    caps = [e for e in edges if e.kind == "line" and abs(e.length - thickness) < 1e-3]
    cap_points = [p for c in caps for p in (c.start, c.end)]
    found = []
    for side in _split_into_sides(edges, caps, tol):
        ends = [p for p, count in _endpoint_counts(side, tol) if count == 1]
        if len(ends) != 2 or not all(any(_dist(p, q) <= tol for q in cap_points) for p in ends):
            continue
        chain = _order_chain(side, ends[0], tol)
        if chain is None or not any(e.kind == "arc" for e in chain):
            continue
        if chain[0].kind != "line" or chain[-1].kind != "line":
            continue
        if any(a.kind == b.kind for a, b in zip(chain, chain[1:])):
            continue
        if any(e.kind == "arc" and (not _tangent(chain[k - 1], e) or not _tangent(chain[k + 1], e))
               for k, e in enumerate(chain)):
            continue
        found.append(chain)
    if len(found) != 1:
        raise _RecoverError(f"expected 1 whole face between two caps, found {len(found)}")

    chain = found[0]
    # la lamiera sta dal lato dell'altro capo del tappo da cui parte la faccia
    first = chain[0]
    cap = next(c for c in caps if c.touches(first.start, tol))
    sheet_side = _side(first, cap.other(first.start))
    cl_lines = [e.length for e in chain if e.kind == "line"]
    cl_turns: List[float] = []
    cl_setbacks: List[float] = []
    for k, e in enumerate(chain):
        if e.kind == "arc":
            partner = _partner(e, edges, thickness)
            if partner is not None:
                r_cl = (e.radius + partner.radius) / 2.0
            elif _side(chain[k - 1], e.center) == sheet_side:
                r_cl = e.radius - thickness / 2.0      # faccia esterna: il centro sta dal lato della lamiera
            else:
                r_cl = e.radius + thickness / 2.0      # faccia interna
            if r_cl <= 0:
                raise _RecoverError("arc smaller than half the thickness on the sheet side")
            sweep = _sweep_deg(e.a0, e.a1, e.ccw)
            cl_turns.append(sweep)
            cl_setbacks.append(r_cl * math.tan(math.radians(abs(sweep)) / 2.0))
    return _compose(cl_lines, cl_turns, cl_setbacks)


def _side(line: _Edge, p: Point) -> int:
    """+1 se `p` sta a sinistra della retta percorsa da start a end, -1 a destra."""
    cross = ((line.end[0] - line.start[0]) * (p[1] - line.start[1])
             - (line.end[1] - line.start[1]) * (p[0] - line.start[0]))
    return 1 if cross > 0 else -1


def _tangent(line: _Edge, arc: _Edge) -> bool:
    """La retta tocca l'arco in un suo capo ed è perpendicolare al raggio lì."""
    p = next((q for q in (line.start, line.end)
              if _dist(q, arc.start) <= 1e-3 or _dist(q, arc.end) <= 1e-3), None)
    if p is None:
        return False
    rx, ry = p[0] - arc.center[0], p[1] - arc.center[1]
    lx, ly = line.end[0] - line.start[0], line.end[1] - line.start[1]
    return abs(rx * lx + ry * ly) <= 1e-2 * math.hypot(rx, ry) * math.hypot(lx, ly)


def _canonical(segments: List[float], angles: List[float]):
    """A section reads the same from either end. Pick a deterministic
    orientation: the one whose segment list sorts first. Reversing also
    flips every angle (a -> 360 - a), because each turn changes sign."""
    fwd = (segments, angles)
    rev = (list(reversed(segments)),
           [round((360.0 - a) % 360.0, 4) for a in reversed(angles)])
    return min(fwd, rev, key=lambda pair: (pair[0], pair[1]))


def _split_into_sides(edges: List[_Edge], caps: List[_Edge], tol: float):
    body = [e for e in edges if e not in caps]
    remaining = list(body)
    sides = []
    while remaining:
        chain = [remaining.pop()]
        grew = True
        while grew:
            grew = False
            # da TUTTI i capi già raccolti, non solo chain[0]/chain[-1]: gli
            # spigoli si accodano nell'ordine in cui si trovano, non lungo la faccia
            for e in list(remaining):
                if any(e.touches(p, tol) for c in chain for p in (c.start, c.end)):
                    chain.append(e)
                    remaining.remove(e)
                    grew = True
        sides.append(chain)
    return sides


def _endpoint_counts(chain: List[_Edge], tol: float):
    pts: List[Point] = []
    for e in chain:
        pts += [e.start, e.end]
    uniq: List[List] = []
    for p in pts:
        hit = next((u for u in uniq if _dist(u[0], p) <= tol), None)
        if hit:
            hit[1] += 1
        else:
            uniq.append([p, 1])
    return uniq


def _order_chain(chain: List[_Edge], start: Point, tol: float):
    ends = {tuple(round(x, 4) for x in p): c for p, c in _endpoint_counts(chain, tol)}
    if not any(_dist(start, p) <= tol for p, _ in _endpoint_counts(chain, tol)):
        return None
    ordered: List[_Edge] = []
    pool = list(chain)
    cur = start
    while pool:
        nxt = next((e for e in pool if e.touches(cur, tol)), None)
        if nxt is None:
            return None
        pool.remove(nxt)
        if _dist(cur, nxt.start) > _dist(cur, nxt.end):
            nxt.start, nxt.end = nxt.end, nxt.start
            if nxt.kind == "arc":
                nxt.a0, nxt.a1 = nxt.a1, nxt.a0
                nxt.ccw = not nxt.ccw
        ordered.append(nxt)
        cur = nxt.end
    return ordered


def _chain_vertex(chain: List[_Edge], k: int, tol: float) -> Point:
    if k == 0:
        return chain[0].start
    return chain[k - 1].end
