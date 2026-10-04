"""
snapbend/flat/holes.py
----------------------
Foro filettato: il significato che snapbend dà a un arco attorno a un cerchio.
Il fatto geometrico (arco concentrico, angolo, rapporto dei raggi) è di forge,
`forge.geometry.arcs_around` (forge MAP.md D91); qui restano le soglie.

    is_threaded_hole — True se il cerchio è un foro filettato
"""

from typing import Tuple

from forge.core.geometry import arcs_around
from forge.core.primitives.segments import ArcSeg
from snapbend.flat.thresholds import THREADED_ARC_MAX_RADIUS_RATIO


def is_threaded_hole(
    center:           Tuple[float, float],
    radius:           float,
    all_arcs:         list[ArcSeg],
    tolerance_center: float = 1.0,
    angle_tolerance:  float = 35.0,
    max_radius_ratio: float = THREADED_ARC_MAX_RADIUS_RATIO,
) -> bool:
    """
    True se attorno al cerchio c'è un arco a ~270° (entro ``angle_tolerance``
    gradi) con raggio fino a ``radius * max_radius_ratio``: l'anello di cresta
    della filettatura. Un arco molto più grande (bordo di una flangia tonda,
    estremità raggiata di un profilo) gira attorno al foro ma non è un filetto.
    """
    return any(abs(a.sweep - 270.0) < angle_tolerance and a.radius_ratio <= max_radius_ratio
               for a in arcs_around(center, radius, all_arcs, tolerance=tolerance_center))
