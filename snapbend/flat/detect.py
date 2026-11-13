"""
snapbend/flat/detect.py
-----------------------
`detect_flat()`: la lettura di processo di un pezzo piano visto dalla sua
faccia (file di taglio / sviluppo) — fori, pieghe, incisioni, sopra il
risultato di `topo.heal()`. Arrivato da topo (topo MAP.md D88).
"""

from __future__ import annotations

from typing import Optional

import topo
from .roles import HOLE, COUNTERSINK, THREADED_HOLE, BEND, ENGRAVE, MARKING, INVALID, is_structural
from .model import (
    BendingLine,
    ClassifiedEntity,
    Engraving,
    HOLE_TYPE_PLAIN,
    HOLE_TYPE_COUNTERSINK,
    HOLE_TYPE_THREADED,
)
from .holes import is_threaded_hole
from .thresholds import HOLE_DIAMETER_THRESHOLD

# Tolleranza per raggruppare le bending line collineari in un'unica piega
# logica. Era `_BENDING_GROUP_TOLERANCE` su `Cluster.summary` prima del
# refactor detect-overlay — `describe_features()` ha preso il posto di quella
# property (MAP.md D8, D44).
_BENDING_GROUP_TOLERANCE = 0.1


def _ensure_overlay(cluster: topo.Cluster) -> topo.Overlay:
    """`cluster.overlay`, creandolo alla prima scrittura."""
    if cluster.overlay is None:
        cluster.overlay = topo.Overlay()
    return cluster.overlay


# Ruoli che detect_flat() sa collocare come feature di un cluster. Un proxy con un
# ruolo deciso ma fuori da qui — frame, title_block, o uno slug di un
# consumatore — è arredo del disegno: heal() l'ha messo in `loose` e detect_flat() ce
# lo lascia, geometria e ruolo intatti (D27, D30). Prima detect_flat() ne faceva un
# ClassifiedEntity scollegato che l'exporter non riscriveva → geometria persa.
_DETECT_KNOWN_ROLES = frozenset({
    HOLE,
    COUNTERSINK,
    THREADED_HOLE,
    ENGRAVE,
    BEND,
    MARKING,
})


# Lane geometriche attivabili da detect_flat(). `detect_flat(result)` nudo non ne esegue
# nessuna: fa solo la lane dei ruoli assegnati al load (role_rules) + la pulizia topologia.
ALL_FEATURES = frozenset({"holes", "bending", "engrave"})


def _normalize_features(features) -> frozenset:
    """
    Normalizza l'argomento `features` di detect_flat() in un set di stringhe.

    Accetta: None/() → nessuna lane; True o "all"/"*" → tutte;
    una stringa singola ("holes"); un iterabile di stringhe.
    """
    if features is None:
        return frozenset()
    if features is True:
        return ALL_FEATURES
    if isinstance(features, str):
        f = features.strip().lower()
        return ALL_FEATURES if f in ("all", "*") else frozenset({f})
    return frozenset(str(f).strip().lower() for f in features)


def _proxy_pts(proxy) -> list:
    """Vertici di un proxy aperto (OpenCurve), derivati dai suoi segmenti nativi."""
    return topo.geometry.track_points(getattr(proxy, "segments", []) or [])

_ROLE_TO_HOLE_TYPE = {
    COUNTERSINK:   HOLE_TYPE_COUNTERSINK,
    THREADED_HOLE: HOLE_TYPE_THREADED,
}


_TOUCH_EPS = 1e-6   # mm — rumore di `topo.geometry.gap`: "tocca" è distanza <= questo, mai == 0


def _release_touching_rings(result: topo.Result) -> None:
    """
    Un `inner` senza ruolo che tocca l'outer non è un contorno interno del
    pezzo: un vuoto non può avere bordo in comune con l'esterno. È un anello
    di tratti non-contorno che topo ha chiuso da sé (vaschetta: le quattro
    pieghe attorno alla base). Si toglie da `cluster.inners` e i suoi lati
    tornano in `result.loose`, una `OpenCurve` per lato: ci arrivano le lane
    come per ogni altra curva sciolta, senza un secondo percorso con gli
    stessi criteri. I discendenti salgono di un livello (la parità della
    profondità decide l'area, D89 di topo). Un inner con un ruolo deciso (un
    foro etichettato) non si tocca.
    """
    for index, cluster in enumerate(result.clusters):
        for ring in list(cluster.inners):
            if ring.depth != 1 or ring.role != topo.model.ContourRole.INNER:
                continue
            if topo.geometry.gap(ring, cluster.outer).distance > _TOUCH_EPS:
                continue
            cluster.inners.remove(ring)
            for inner in cluster.inners:
                node = inner
                while node is not None and node is not ring:
                    node = node.parent
                if node is ring:
                    inner.depth -= 1
                    if inner.parent is ring:
                        inner.parent = ring.parent
            result.loose += [
                topo.model.OpenCurve(role=topo.model.ContourRole.UNKNOWN,
                                     segments=[seg], cluster_ref=index)
                for seg in ring.segments
            ]


def _mark_invalid_inners(result: topo.Result, min_distance: float) -> None:
    """
    Un `inner` senza ruolo a meno di `min_distance` mm dall'outer (misura:
    `topo.geometry.gap`) diventa un `Invalid(reason="inner-too-close")` in
    `cluster.overlay["invalid"]`, e sparisce da `cluster.inners` come un foro
    promosso: non è più un foro candidato e nel DXF va sul layer `Invalid`.
    Resta un vuoto (`is_void`), l'area netta non cambia. La soglia è del
    chiamante, snapbend non ne ha una. Un inner con un ruolo deciso dal
    chiamante non si tocca. Un `Diagnostic` dice dove, in `result.warnings`.
    """
    from .model import Invalid, REASON_INNER_TOO_CLOSE
    points = []
    for cluster in result.clusters:
        kept = []
        for inner in cluster.inners:
            gap = None
            if inner.depth == 1 and inner.role == topo.model.ContourRole.INNER:
                gap = topo.geometry.gap(inner, cluster.outer)
            if gap is None or gap.distance >= min_distance:
                kept.append(inner)
                continue
            _ensure_overlay(cluster).add("invalid", Invalid(
                role=INVALID, segments=list(inner.segments), styles=list(inner.styles or []),
                reason=REASON_INNER_TOO_CLOSE, distance=gap.distance,
            ))
            points.append(gap.on_a)
        cluster.inners = kept
    if points:
        result.warnings.append(topo.Diagnostic(
            REASON_INNER_TOO_CLOSE,
            f"{len(points)} inner contour(s) closer than {min_distance} mm to the outer, "
            f"in the overlay as 'invalid'",
            points=points,
            help="detect_flat(result, min_inner_distance=...) with a smaller limit",
        ))


# ---------------------------------------------------------------------------
# API pubblica
# ---------------------------------------------------------------------------

def detect_flat(
    doc:               topo.Document,
    features=None,
    *,
    tolerance:         Optional[float] = None,
    max_gap:           Optional[float] = None,
    label:             str = "",
    source_file:       str = "",
    max_drill_diameter: float = HOLE_DIAMETER_THRESHOLD,
    bending_tolerance: float = 1.0,
    engrave_tolerance: float = 1.0,
    min_inner_distance: Optional[float] = None,
) -> topo.Result:
    """
    Legge un pezzo piano (file di taglio, sviluppo) dal `Document` di topo:
    `topo.heal(doc, is_structural=snapbend.flat.is_structural).faces()` e poi
    la classificazione delle feature dentro le parti trovate. L'unico
    ingresso: il predicato strutturale di processo (un foro è un contorno di
    pezzo) lo passa lei, nessuno può dimenticarlo (MAP.md D78).

    `tolerance`, `max_gap`, `label`, `source_file` sono le opzioni di
    `topo.heal` (stessi default). Se il documento non dà parti valide il
    `Result` torna comunque, con `is_valid=False`, e le lane non girano.

    `detect_flat(doc)` nudo esegue solo la lane dei ruoli assegnati al load (`role_rules`) e la
    pulizia della topologia: i contorni circolari restano `inners`, nessun
    `Hole`. È il default per il taglio laser (`laser-cutting-default`).

    Le lane geometriche sono opt-in via `features`:
        detect_flat(doc, "holes")           → promozione fori (Ø < max_drill_diameter)
        detect_flat(doc, "all")             → fori + pieghe + incisioni
        detect_flat(doc, {"holes", "bending"})

    `max_drill_diameter` (default `HOLE_DIAMETER_THRESHOLD`, 32.1 mm) è un
    parametro di processo: sotto soglia il contorno circolare è un foro da
    punta, sopra resta un contorno interno.

    `min_inner_distance` (mm, default `None` = nessun limite): un contorno
    interno senza ruolo più vicino di così all'outer diventa un
    `Invalid` in `cluster.overlay["invalid"]` (layer `Invalid`) e non un foro. È la scelta
    del chiamante, snapbend non ne propone una: nessun valore, nessun
    controllo. Diverso dal "tocca" (distanza <= 1e-6), che è sempre invalido
    e sempre letto (un anello che tocca l'outer torna in `loose`).
    """
    result = topo.heal(doc, tolerance=tolerance, max_gap=max_gap, label=label,
                       source_file=source_file, is_structural=is_structural).faces()
    if not (result.is_valid and result.clusters):
        return result
    return _detect_in_result(
        result, features,
        max_drill_diameter=max_drill_diameter, bending_tolerance=bending_tolerance,
        engrave_tolerance=engrave_tolerance, min_inner_distance=min_inner_distance,
    )


def _detect_in_result(
    result:             topo.Result,
    features,
    *,
    max_drill_diameter: float = HOLE_DIAMETER_THRESHOLD,
    bending_tolerance:  float = 1.0,
    engrave_tolerance:  float = 1.0,
    min_inner_distance: Optional[float] = None,
) -> topo.Result:
    """Le lane di `detect_flat()` su un `Result` già letto. Muta `result` e lo ritorna."""
    feats = _normalize_features(features)

    _release_touching_rings(result)
    _detect_labeled(result)
    if min_inner_distance is not None:
        _mark_invalid_inners(result, min_inner_distance)
    if "bending" in feats:
        _detect_bending(result, bending_tolerance=bending_tolerance)
    if "engrave" in feats:
        _detect_engrave(result, engrave_tolerance=engrave_tolerance)
    if "holes" in feats:
        _detect_holes(result, max_drill_diameter=max_drill_diameter)
    return result


def describe_features(cluster: topo.Cluster) -> dict:
    """
    Conteggio ricco per i tipi **noti di topo** — fori per tipo, pieghe
    raggruppate, lunghezza incisioni/marcature. Era `Cluster.summary`
    per intero prima del refactor detect-overlay (MAP.md D8, D44): si è
    spostato qui perché serve le costanti `HOLE_TYPE_*`, che `model/` non può
    importare da `tools/`.

    Non sostituisce `cluster.summary` (property, generica, sempre
    disponibile anche con solo `heal()`): è un livello in più sopra, per chi
    vuole il dettaglio dei tipi che solo topo sa riconoscere. Un tool
    esterno che attacca un suo nome custom a `cluster.overlay` non compare
    qui — compare già in `cluster.summary` come conteggio grezzo.
    """
    holes         = cluster.features("holes")
    bending_lines = cluster.features("bending_lines")
    engrave_lines = cluster.features("engrave_lines")

    from collections import Counter
    htypes = Counter(h.hole_type for h in holes)

    bending_groups = (
        len(topo.geometry.group_collinear_lines(
            bending_lines,
            tolerance=_BENDING_GROUP_TOLERANCE,
        ))
        if bending_lines else 0
    )

    marking = cluster.features("marking_entities")

    return {
        "plain_holes_count":    htypes.get(HOLE_TYPE_PLAIN, 0),
        "countersink_count":    htypes.get(HOLE_TYPE_COUNTERSINK, 0),
        "threaded_holes_count": htypes.get(HOLE_TYPE_THREADED, 0),
        "bending_lines":        bending_groups,
        "total_engrave_length": round(
            sum(e.length or 0.0 for e in engrave_lines), 4
        ),
        "total_marking_length": round(
            sum(m.get("length") or 0.0 for m in marking), 4
        ),
    }


# ---------------------------------------------------------------------------
# Step 1 — labeled shapes
# ---------------------------------------------------------------------------

def _detect_labeled(result: topo.Result) -> None:
    classified_ids = set()

    for proxy in result.loose:
        if proxy.role == topo.model.ContourRole.UNKNOWN:
            continue
        if proxy.role not in _DETECT_KNOWN_ROLES:
            # Arredo del disegno o ruolo di un consumatore: resta in `loose`,
            # geometria e ruolo intatti, riscritto in output (D27, D30).
            continue

        is_closed = isinstance(proxy, topo.model.ClosedCurve)

        if proxy.role == ENGRAVE:
            placed = (
                _handle_engrave_closed_loose(proxy, result) if is_closed
                else _handle_engrave_open(proxy, result)
            )
            if placed:
                classified_ids.add(id(proxy))
            continue

        if is_closed:
            work_type = topo.model.role_str(proxy.role)
            data = _extract_data_from_source(work_type, proxy)
            rep  = data.pop("representative_point", None)
            ce = ClassifiedEntity(
                work_type=work_type,
                confidence=1.0,
                source="labeled",
                data=data,
                representative_point=rep,
                curve=proxy,
            )
            if _assign_to_part(ce, result):
                classified_ids.add(id(proxy))
            continue

        work_type = topo.model.role_str(proxy.role)
        data = _extract_data(proxy, work_type)
        rep  = data.pop("representative_point", None)
        ce   = ClassifiedEntity(
            work_type=work_type,
            confidence=1.0,
            source="labeled",
            data=data,
            representative_point=rep,
            curve=proxy if len(_proxy_pts(proxy)) >= 2 else None,
        )
        if _assign_to_part(ce, result):
            classified_ids.add(id(proxy))

    result.loose = [
        p for p in result.loose if id(p) not in classified_ids
    ]

    _LABELED_HOLE_ROLES = (
        HOLE, COUNTERSINK, THREADED_HOLE,
    )

    for cluster in result.clusters:
        remaining = []
        for inner in cluster.inners:
            # Lane dei ruoli assegnati al load: un contorno con ruolo foro
            # assegnato da role_rules diventa un Hole a prescindere dai
            # `features` richiesti (D15).
            if inner.role in _LABELED_HOLE_ROLES:
                _ensure_overlay(cluster).add("holes", _labeled_hole_from_contour(inner))
                continue

            if inner.role == topo.model.ContourRole.UNKNOWN or topo.model.is_structural_role(inner.role):
                remaining.append(inner)
                continue

            if inner.role not in _DETECT_KNOWN_ROLES:
                # Ruolo di un consumatore su un loop interno: topo non lo
                # classifica, resta un inner del cluster (D27, D30).
                remaining.append(inner)
                continue

            if inner.role == ENGRAVE:
                _handle_engrave_closed(inner, cluster)
                continue

            work_type = topo.model.role_str(inner.role)
            data = _extract_data_from_source(work_type, inner)
            rep  = data.pop("representative_point", None)
            ce = ClassifiedEntity(
                work_type=work_type,
                confidence=1.0,
                source="labeled",
                data=data,
                representative_point=rep,
                curve=inner,
            )
            if not _assign_to_part(ce, result):
                remaining.append(inner)
        cluster.inners = remaining


# ---------------------------------------------------------------------------
# Step 2 — bending geometrico
# ---------------------------------------------------------------------------

# Di quanto si prolunga una candidata piega ai due capi prima di vedere se
# taglia il pezzo (snapbend MAP.md D52).
_BEND_REACH = 1.0

# Due tratti stanno sulla stessa retta se la direzione differisce meno di
# questo (radianti) e la distanza fra le rette meno di _BEND_LINE_OFFSET (mm).
_BEND_ANGLE_TOL = 1e-3
_BEND_LINE_OFFSET = 0.1


def _bending_line(cluster, start, end, length, source="geometric"):
    return BendingLine(
        role=BEND,
        start=tuple(start[:2]),
        end=tuple(end[:2]),
        length=length,
        angle_deg=topo.geometry.chord_angle_deg(start, end),
        cluster_label=cluster.label,
        source=source,
        confidence=0.9,
    )


def _detect_bending(result: topo.Result, bending_tolerance: float = 1.0) -> None:
    """
    Una piega attraversa il pezzo (`topo.geometry.splits_contour`, prolungata di
    `_BEND_REACH`). Se un vuoto la interrompe,
    i tratti sulla stessa retta separati solo da vuoti valgono come una
    piega: la retta che li unisce deve attraversare il pezzo, e sul layer
    vanno i tratti disegnati (snapbend MAP.md D53).
    """
    leftovers: dict = {}   # id(cluster) -> [(start, end, proxy)]

    for proxy in list(result.loose):
        if proxy.cluster_ref is None:
            continue
        pts = _proxy_pts(proxy)
        if len(pts) != 2:   # una retta ha due punti (topo D176)
            continue
        length = topo.geometry.track_length(pts)
        if length < bending_tolerance:
            continue

        cluster = result.clusters[proxy.cluster_ref]
        if topo.geometry.splits_contour(cluster.outer, pts[0], pts[-1], reach=_BEND_REACH):
            result.promote(proxy, cluster, "bending_lines",
                           item=_bending_line(cluster, pts[0], pts[-1], length))
        else:
            leftovers.setdefault(id(cluster), []).append((pts[0], pts[-1], proxy))

    for cluster in result.clusters:
        pieces = leftovers.get(id(cluster))
        if not pieces or not cluster.inners:
            continue
        voids = [i for i in cluster.inners if i.depth % 2]
        runs = topo.geometry.bridged_runs([p[:2] for p in pieces], voids,
                            tolerance=_BEND_LINE_OFFSET, angle_tolerance=_BEND_ANGLE_TOL)
        for run in runs:
            if not topo.geometry.splits_contour(cluster.outer, run.start, run.end, reach=_BEND_REACH):
                continue
            for proxy in (pieces[j][2] for j in run.members):
                pts = _proxy_pts(proxy)
                # `promote` toglie la linea da `loose`: to_dxf non la scrive
                # due volte (una come piega, una come curva sciolta)
                result.promote(proxy, cluster, "bending_lines", item=_bending_line(
                    cluster, pts[0], pts[-1], topo.geometry.track_length(pts)))


# ---------------------------------------------------------------------------
# Step 3 — promozione fori
# ---------------------------------------------------------------------------

_CONCENTRIC_TOLERANCE = 1.0   # mm — distanza max fra i centri per un countersink


def _detect_holes(result: topo.Result, max_drill_diameter: float = HOLE_DIAMETER_THRESHOLD) -> None:
    """
    Lane geometrica: promuove a `Hole` i contorni interni circolari.

    heal() non produce più `Hole` (D15): consegna solo l'albero di contenimento
    con `cluster.inners` piatto. Qui:
      - coppie concentriche (cerchio piccolo dentro cerchio grande) → countersink
        (il piccolo diventa `Hole`, l'anello grande viene assorbito);
      - contorni circolari con Ø < `max_drill_diameter` → foro (plain / threaded);
      - Ø >= `max_drill_diameter` → restano `Contour` in `cluster.inners`.
    """
    arcs = _result_arcs(result)
    for cluster in result.clusters:
        _promote_geometric_holes(cluster, arcs, max_drill_diameter)


def _result_arcs(result: topo.Result) -> list[topo.primitives.ArcSeg]:
    """
    Ogni arco del risultato: ogni curva è contorno di un cluster o sta in
    `loose` (topo D137), quindi gli archi sono tutti lì. Le creste dei
    filetti, archi aperti, stanno in `loose`.
    """
    curves = [c.outer for c in result.clusters]
    curves += [i for c in result.clusters for i in c.inners]
    curves += result.loose
    return [s for cv in curves for s in cv.segments
            if isinstance(s, topo.primitives.ArcSeg)]


def _circle(contour) -> tuple[Optional[float], Optional[tuple]]:
    """(diametro, centro) se il contorno è un cerchio per `topo.geometry.contour_shape`,
    altrimenti (None, None). Misura esatta dalle primitive, non dal bounding box
    del poligono discretizzato (MAP.md D66)."""
    shape = topo.geometry.contour_shape(contour)
    if shape is None or shape.kind != "circle":
        return None, None
    return shape.diameter, shape.center


def _circular_inners(cluster: topo.Cluster) -> list:
    """(contour, diameter, center) per ogni inner geometricamente circolare."""
    out = []
    for c in cluster.inners:
        if c.role not in (topo.model.ContourRole.UNKNOWN, topo.model.ContourRole.INNER):
            continue
        dia, ctr = _circle(c)
        if dia is not None:
            out.append((c, dia, ctr))
    return out


def _promote_geometric_holes(cluster: topo.Cluster,
                             arcs: list[topo.primitives.ArcSeg],
                             max_drill_diameter: float) -> None:
    circ = _circular_inners(cluster)
    if not circ:
        return

    swallowed: set = set()      # id(contour) degli anelli esterni di countersink
    promoted:  dict = {}        # id(contour) -> Hole

    # --- countersink: nel gruppo concentrico (topo D91) ogni cerchio si
    #     accoppia col più piccolo dei cerchi più grandi ancora liberi ---
    by_id = {id(c): (c, d, ctr) for c, d, ctr in circ}
    for group in topo.geometry.concentric_groups([c for c, _, _ in circ], tolerance=_CONCENTRIC_TOLERANCE):
        members = [by_id[id(c)] for c in group.items]
        for i, (inner_c, inner_d, inner_ctr) in enumerate(members):
            if id(inner_c) in swallowed:
                continue
            outer = next((m for m in members[i + 1:]
                          if m[1] > inner_d and id(m[0]) not in swallowed
                          and topo.to_shapely(m[0]).contains(topo.to_shapely(inner_c))), None)
            if outer is None:
                continue
            swallowed.add(id(outer[0]))
            promoted[id(inner_c)] = _hole_from_contour(
                inner_c, inner_d, inner_ctr,
                hole_type=HOLE_TYPE_COUNTERSINK, confidence=0.85,
                geometric_hint="countersink", outer_diameter=outer[1],
            )

    # --- fori piatti / filettati ---
    for c, dia, ctr in circ:
        if id(c) in promoted or id(c) in swallowed:
            continue
        if dia >= max_drill_diameter:
            continue    # sopra la capacità di foratura → resta contorno interno
        threaded = is_threaded_hole(
            center=ctr, radius=dia / 2, all_arcs=arcs,
        )
        promoted[id(c)] = _hole_from_contour(
            c, dia, ctr,
            hole_type=HOLE_TYPE_THREADED if threaded else HOLE_TYPE_PLAIN,
            confidence=0.80 if threaded else 1.0,
        )

    if not promoted and not swallowed:
        return

    new_inners = []
    for c in cluster.inners:
        if id(c) in swallowed:
            continue
        hole = promoted.get(id(c))
        if hole is not None:
            _ensure_overlay(cluster).add("holes", hole)
        else:
            new_inners.append(c)
    cluster.inners = new_inners


def _hole_from_contour(contour, diameter, center, *, hole_type, confidence,
                       geometric_hint="", outer_diameter=None):
    from .model import Hole
    return Hole(
        role=HOLE,
        segments=list(getattr(contour, "segments", []) or []),
        styles=list(getattr(contour, "styles", []) or []),
        diameter=diameter,
        center=center,
        hole_type=hole_type,
        geometric_hint=geometric_hint,
        confidence=confidence,
        source="geometric",
        outer_diameter=outer_diameter,
    )


def _labeled_hole_from_contour(contour):
    """`Contour` con ruolo foro da role_rules → `Hole(source="labeled")`."""
    from .model import Hole

    dia, ctr = _circle(contour)
    hole_type = _ROLE_TO_HOLE_TYPE.get(contour.role, HOLE_TYPE_PLAIN)
    return Hole(
        role=contour.role,
        segments=list(getattr(contour, "segments", []) or []),
        styles=list(getattr(contour, "styles", []) or []),
        diameter=dia or 0.0,
        center=ctr or (0.0, 0.0),
        hole_type=hole_type,
        confidence=1.0,
        source="labeled",
    )


# ---------------------------------------------------------------------------
# Step — inferenza engrave (PLACEHOLDER)
# ---------------------------------------------------------------------------

def _detect_engrave(result: topo.Result, engrave_tolerance: float = 1.0) -> None:
    """
    Inferenza geometrica delle incisioni — NON ANCORA IMPLEMENTATA.

    Stesso pattern di `_detect_holes` / `_detect_bending`: le incisioni con
    ruolo esplicito (role_rules) sono già state promosse da `_detect_labeled`
    con `source="labeled"`. Qui si guarda ciò che è rimasto non etichettato —
    `cluster.inners` con role UNKNOWN e `result.loose` — e si promuove a
    `Engraving(source="geometric")` quello che geometricamente È un'incisione,
    es.:
      - inner contour costituito da due polilinee ~parallele a distanza
        < engrave_tolerance → traccia di incisione, non un inner/foro
      - coppie di segmenti aperti ravvicinati e paralleli in `loose`

    Finché è un placeholder non muta nulla.
    """
    return


# ---------------------------------------------------------------------------
# Engrave handlers
# ---------------------------------------------------------------------------

def _engraving_from_open(proxy, cluster_label: str = "",
                         source: str = "labeled", confidence: float = 1.0) -> Engraving:
    pts = _proxy_pts(proxy)
    return Engraving(
        role=ENGRAVE,
        segments=list(getattr(proxy, "segments", []) or []),
        styles=list(getattr(proxy, "styles", []) or []),
        length=round(topo.geometry.track_length(pts), 4),
        pts=pts,
        cluster_label=cluster_label,
        source=source,
        confidence=confidence,
    )


def _engraving_from_closed(curve, cluster_label: str = "",
                           source: str = "labeled", confidence: float = 1.0) -> Engraving:
    return Engraving(
        role=ENGRAVE,
        segments=list(curve.segments or []),
        styles=list(curve.styles or []),
        length=round(_perimeter(curve), 4),
        pts=curve.points(),
        closed=True,
        cluster_label=cluster_label,
        source=source,
        confidence=confidence,
    )


def _handle_engrave_open(proxy: topo.model.OpenCurve, result: topo.Result) -> bool:
    """
    Una traccia engrave aperta va al cluster che la contiene
    (`proxy.cluster_ref`, topo D137) → cluster.engrave_lines (ritorna True).
    Fuori da ogni cluster → resta in `loose`: è geometria orfana come ogni
    altra entità che non sta dentro un outer (ritorna False).
    """
    if proxy.cluster_ref is None:
        return False
    cluster = result.clusters[proxy.cluster_ref]
    _ensure_overlay(cluster).add(
        "engrave_lines", _engraving_from_open(proxy, cluster_label=cluster.label)
    )
    return True


def _handle_engrave_closed_loose(proxy, result: topo.Result) -> bool:
    """
    Come _handle_engrave_open ma per una traccia engrave già chiusa
    (CIRCLE / SPLINE chiusa su layer engrave).
    """
    if proxy.cluster_ref is None:
        return False
    cluster = result.clusters[proxy.cluster_ref]
    _ensure_overlay(cluster).add("engrave_lines", _engraving_from_closed(
        proxy, cluster_label=cluster.label))
    return True


def _handle_engrave_closed(inner, cluster: topo.Cluster) -> None:
    _ensure_overlay(cluster).add("engrave_lines", _engraving_from_closed(
        inner, cluster_label=cluster.label))


# ---------------------------------------------------------------------------
# Assegnazione al cluster contenitore
# ---------------------------------------------------------------------------

_LABEL_COVER_EPS = 1e-3  # mm — precisione geometrica, non tolleranza utente (v. MAP.md D54)


def _belongs_to_cluster(ce: ClassifiedEntity, cluster: topo.Cluster) -> bool:
    """
    Un'entità aperta (marking/bending) appartiene al cluster se la sua
    geometria INTERA è coperta dal contorno outer — non solo un punto
    rappresentativo: quello fallisce per costruzione su un'entità che giace
    esattamente sul bordo, il caso comune di una piega o una marcatura
    tracciata proprio sul lato del pezzo. Il buffer è una domanda fra due
    geometrie: passa da `topo.to_shapely` (topo D168).
    """
    if isinstance(ce.curve, topo.model.OpenCurve):
        return topo.to_shapely(cluster.outer).buffer(_LABEL_COVER_EPS).covers(topo.to_shapely(ce.curve))
    probe = _probe_point(ce)
    return probe is not None and cluster.outer.contains(probe)


def _assign_to_part(ce: ClassifiedEntity, result: topo.Result) -> bool:
    """
    Scrive `ce` nel cluster che la contiene; False se nessuno la contiene:
    allora la curva da cui viene resta dov'era in `result` (loose o inner),
    così niente sparisce dal risultato di topo (topo D137).
    """
    work_type = ce.work_type.lower()

    for cluster in result.clusters:
        if not _belongs_to_cluster(ce, cluster):
            continue

        if work_type == "bending":
            _ensure_overlay(cluster).add(
                "bending_lines", _bending_line_from_data(ce.data, cluster.label)
            )

        _write_entity(ce, cluster)
        return True

    result.warnings.append(topo.Diagnostic(
        "shape-outside-clusters",
        f"{ce.work_type} shape (source={ce.source}) is in no cluster, left in result.loose",
        points=[ce.representative_point] if ce.representative_point else (),
    ))
    return False


def _write_entity(ce: ClassifiedEntity, cluster: topo.Cluster) -> None:
    """
    I dati dell'entità nell'overlay, sotto `<tipo>_entities`. La piega no: è
    già un `BendingLine` in `bending_lines` (scritto da `_assign_to_part`).
    `Cluster.custom` non esiste più in topo: l'overlay è il posto.
    """
    work_type = ce.work_type.lower()
    if work_type == "bending":
        return
    _ensure_overlay(cluster).add(f"{work_type}_entities", {
        **ce.data,
        "confidence": ce.confidence,
        "source":     ce.source,
    })


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _probe_point(ce: ClassifiedEntity) -> Optional[tuple]:
    if ce.representative_point is not None:
        return ce.representative_point
    return _centroid(ce.curve) if isinstance(ce.curve, topo.model.ClosedCurve) else None


def _centroid(curve) -> Optional[tuple]:
    """Baricentro esatto della curva chiusa; None se non racchiude area."""
    try:
        return curve.centroid
    except ValueError:
        return None


def _perimeter(curve) -> float:
    return sum(topo.geometry.segment_length(s) for s in curve.segments)


def _extract_data(proxy: topo.model.OpenCurve, work_type: str) -> dict:
    work_type = work_type.lower()
    pts = _proxy_pts(proxy)
    length = topo.geometry.track_length(pts)

    if len(pts) >= 2:
        rep = (
            sum(p[0] for p in pts) / len(pts),
            sum(p[1] for p in pts) / len(pts),
        )
    else:
        rep = pts[0] if pts else None

    if work_type == "bending" and len(pts) == 2:
        start = pts[0]
        end   = pts[-1]
        return {
            "start":                start,
            "end":                  end,
            "length":               round(length, 4),
            "angle_deg":            round(topo.geometry.chord_angle_deg(start, end), 4),
            "representative_point": rep,
        }

    if work_type == "marking":
        return {
            "length":               round(length, 4),
            "representative_point": rep,
        }

    return {"representative_point": rep}


def _extract_data_from_source(work_type: str, curve) -> dict:
    """Dati di un'entità chiusa (`ClosedCurve`) letti sui suoi segmenti."""
    work_type = work_type.lower()
    rep = _centroid(curve)

    if work_type == "marking":
        length = round(_perimeter(curve), 4)
        return {
            "length":               length,
            "representative_point": rep,
        }

    return {"representative_point": rep}


def _bending_line_from_data(data: dict, cluster_label: str) -> BendingLine:
    start = data["start"]
    end   = data["end"]
    return BendingLine(
        role=BEND,
        start=tuple(start[:2]),
        end=tuple(end[:2]),
        length=data["length"],
        angle_deg=data["angle_deg"],
        cluster_label=cluster_label,
        source="labeled",
        confidence=1.0,
    )