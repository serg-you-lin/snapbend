"""
snapbend/flat/model/bending_line.py
-----------------------------------
Linea di piega letta da `detect_flat()` (arrivata da forge, forge MAP.md D88).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from shapely.geometry import LineString

from forge.core.primitives import LineSeg
from forge.model.feature import OpenFeature
from forge.model.role import ContourRole
from snapbend.flat.roles import BEND
from .render import RenderContour


@dataclass
class BendingLine(OpenFeature):
    geometry:   LineString    = field(default=None)
    length:     float         = 0.0
    angle_deg:  float         = 0.0
    cluster_label: str           = ""
    # Doppio binario di provenienza, come Hole ed Engraving (MAP.md D5):
    #   source="labeled"   → ruolo da role_rules       (confidence 1.0)
    #   source="geometric" → inferenza in detect_flat()     (confidence < 1.0)
    confidence: float         = 1.0
    source:     str           = ""

    def __post_init__(self):
        if self.role == ContourRole.UNKNOWN:
            self.role = BEND

    @property
    def contours(self) -> list:
        """Disegno per forge: una LINE dal primo all'ultimo punto."""
        coords = list(self.geometry.coords) if self.geometry is not None else []
        if len(coords) < 2:
            return []
        return [RenderContour(role=self.role, segments=[LineSeg(coords[0], coords[-1])])]

    def to_dict(self) -> dict:
        coords = list(self.geometry.coords)
        return {
            "start":      coords[0],
            "end":        coords[-1],
            "length":     round(self.length, 4),
            "angle_deg":  round(self.angle_deg, 4),
            "cluster_label": self.cluster_label,
            "source":     self.source,
            "confidence": round(self.confidence, 4),
        }
