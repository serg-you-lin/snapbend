"""
snapbend/flat/model/engraving.py
--------------------------------
Incisione rilevata da detect_flat() (arrivata da topo, topo MAP.md D88).

Un solo tipo: `Engraving`. Un'incisione è concettualmente una traccia aperta
(N segmenti su layer engrave). Un contorno chiuso su layer engrave NON viene
riassemblato in un loop unico — resta N segmenti separati (scelta di progetto).
`closed` dice che la traccia era già chiusa in origine (CIRCLE, SPLINE
chiusa): un fatto della sorgente, non un loop strutturale. Nessun tipo
shapely nel modello (topo D168).

Doppio binario di provenienza, identico a Hole:
    source="labeled"   → ruolo assegnato da role_rules al load   (confidence 1.0)
    source="geometric" → inferenza geometrica in detect_flat()        (confidence < 1.0)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

import topo
from snapbend.flat.roles import ENGRAVE
from .render import RenderContour


@dataclass
class Engraving(topo.model.OpenCurve):
    length:     float                    = 0.0
    cluster_label: str                      = ""
    pts:        List[Tuple[float, float]] = field(default_factory=list)
    closed:     bool                     = False
    confidence: float                    = 1.0
    source:     str                      = "labeled"

    def __post_init__(self):
        if self.role == topo.model.ContourRole.UNKNOWN:
            self.role = ENGRAVE

    @property
    def contours(self) -> list:
        """Disegno per topo: N primitive separate, mai un contorno chiuso."""
        return [RenderContour(role=self.role, segments=self.segments, styles=self.styles)]

    def to_dict(self) -> dict:
        d = {
            "closed":     self.closed,
            "length":     round(self.length, 4),
            "cluster_label": self.cluster_label,
            "source":     self.source,
            "confidence": round(self.confidence, 4),
        }
        if self.pts and not self.closed:
            d["start"] = self.pts[0]
            d["end"]   = self.pts[-1]
        return d
