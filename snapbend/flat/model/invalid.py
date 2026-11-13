"""
snapbend/flat/model/invalid.py
------------------------------
Una cosa che `detect_flat()` ha letto e giudica non valida per il processo,
con il motivo: la geometria resta nel file, sul suo layer, e la si vede.
Nasce per un contorno interno troppo vicino all'outer (`min_inner_distance`),
ma è generica: il `reason` (un codice kebab-case, come il `code` di un
`topo.Diagnostic`) dice che cosa non va.
"""
from dataclasses import dataclass
from typing import Optional

import topo
from snapbend.flat.roles import INVALID
from .render import RenderContour

REASON_INNER_TOO_CLOSE = "inner-too-close"


@dataclass
class Invalid(topo.model.ClosedCurve):
    reason:   str             = ""
    distance: Optional[float] = None   # mm, la misura che ha fatto scattare il motivo (se c'è)
    void:     bool            = True   # vuoto del pezzo: conta nell'area netta (come un foro)
    source:   str             = "geometric"

    def __post_init__(self):
        if self.role == topo.model.ContourRole.UNKNOWN:
            self.role = INVALID

    @property
    def is_void(self) -> bool:
        """Per topo (D90): un inner invalido è ancora un vuoto, tolto dall'area."""
        return self.void

    @property
    def contours(self) -> list:
        """Disegno per topo: sul layer `Invalid`, non su quello degli inner."""
        return [RenderContour(role=self.role, segments=self.segments, styles=self.styles)]

    def to_dict(self) -> dict:
        d = {"reason": self.reason, "role": self.role, "source": self.source}
        if self.distance is not None:
            d["distance"] = round(self.distance, 4)
        return d
