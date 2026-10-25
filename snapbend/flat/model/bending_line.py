"""
snapbend/flat/model/bending_line.py
-----------------------------------
Linea di piega letta da `detect_flat()` (arrivata da topo, topo MAP.md D88).
`start`/`end` sono sempre i capi dell'asse intero; `dashes`, se c'è, è come
la piega si disegna (`trim_bending_lines`, MAP.md D63). Un tratto con
`start`/`end` è quello che le funzioni di topo sulle rette accettano
(`group_collinear_lines`, `bridged_runs`, topo D168).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

import topo
from snapbend.flat.roles import BEND
from .render import RenderContour


@dataclass
class BendingLine(topo.model.OpenCurve):
    start:      Tuple[float, float] = (0.0, 0.0)
    end:        Tuple[float, float] = (0.0, 0.0)
    length:     float         = 0.0
    angle_deg:  float         = 0.0
    cluster_label: str           = ""
    # Doppio binario di provenienza, come Hole ed Engraving (MAP.md D5):
    #   source="labeled"   → ruolo da role_rules       (confidence 1.0)
    #   source="geometric" → inferenza in detect_flat()     (confidence < 1.0)
    confidence: float         = 1.0
    source:     str           = ""
    # Tratti con cui la piega si disegna, (start, end) lungo l'asse; vuoto =
    # linea intera. Una piega tratteggiata resta UNA piega (MAP.md D63).
    dashes:     list          = field(default_factory=list)

    def __post_init__(self):
        if self.role == topo.model.ContourRole.UNKNOWN:
            self.role = BEND

    @property
    def contours(self) -> list:
        """Disegno per topo: una LINE da `start` a `end`, o una LINE per tratto."""
        spans = self.dashes or [(self.start, self.end)]
        return [RenderContour(role=self.role, segments=[topo.primitives.LineSeg(a, b)]) for a, b in spans]

    def to_dict(self) -> dict:
        data = {
            "start":      self.start,
            "end":        self.end,
            "length":     round(self.length, 4),
            "angle_deg":  round(self.angle_deg, 4),
            "cluster_label": self.cluster_label,
            "source":     self.source,
            "confidence": round(self.confidence, 4),
        }
        if self.dashes:
            data["dashes"] = [[a, b] for a, b in self.dashes]
        return data
