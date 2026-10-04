"""
snapbend/flat/model/hole.py
---------------------------
Foro letto da `detect_flat()` su un contorno interno di forge (arrivato da
forge, forge MAP.md D88).
"""
from dataclasses import dataclass, field
from typing import Optional, Tuple, Any, List
from shapely.geometry import Polygon

from forge.core.primitives import LineSeg, ArcSeg, CircleSeg, SplineSeg
from forge.model.feature import ClosedFeature
from forge.model.role import ContourRole
from snapbend.flat.roles import HOLE, COUNTERSINK, THREADED_HOLE
from .render import RenderContour

HOLE_TYPE_UNKNOWN      = "unknown"
HOLE_TYPE_PLAIN        = "plain"
HOLE_TYPE_COUNTERSINK  = "countersink"
HOLE_TYPE_THREADED     = "threaded"

VALID_HOLE_TYPES = {
    HOLE_TYPE_UNKNOWN,
    HOLE_TYPE_PLAIN,
    HOLE_TYPE_COUNTERSINK,
    HOLE_TYPE_THREADED,
}


@dataclass
class Hole(ClosedFeature):
    diameter:       float                     = 0.0
    center:         Tuple[float, float]       = field(default_factory=lambda: (0.0, 0.0))
    hole_type:      str                       = HOLE_TYPE_UNKNOWN
    geometric_hint: str                       = ""
    confidence:     float                     = 0.0
    source:         str                       = ""
    origin:         str                       = ""
    outer_diameter:   Optional[float]         = None
    is_hole:          bool                    = True

    def __post_init__(self):
        if self.role == ContourRole.UNKNOWN:
            self.role = HOLE

    @property
    def is_void(self) -> bool:
        """Per forge (D90): un foro è un vuoto del pezzo, conta nell'area netta."""
        return True

    @property
    def contours(self) -> list:
        """Disegno per forge: la svasatura e il filettato hanno il loro layer."""
        role = {HOLE_TYPE_COUNTERSINK: COUNTERSINK,
                HOLE_TYPE_THREADED: THREADED_HOLE}.get(self.hole_type, self.role)
        return [RenderContour(role=role, segments=self.segments,
                              styles=self.styles, polygon=self.polygon)]

    def to_dict(self) -> dict:
        d = {
            "hole_type":  self.hole_type,
            "diameter":   round(self.diameter, 4),
            "center":     (round(self.center[0], 4), round(self.center[1], 4)),
            "role":       self.role,
            "confidence": round(self.confidence, 4),
            "source":     self.source,
        }

        if self.outer_diameter is not None:
            d["outer_diameter"] = round(self.outer_diameter, 4)
        return d