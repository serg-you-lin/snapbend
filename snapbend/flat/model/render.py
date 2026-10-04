"""
snapbend/flat/model/render.py
-----------------------------
Come un elemento di processo si fa disegnare dai renderer di forge.

forge disegna un elemento di `cluster.detected` dal suo `role` e dalla sua
geometria (forge D90): se ha `contours`, ognuno con `role`, `segments`,
`styles`, `polygon`. `polygon` presente → contorno chiuso; assente → una
entità per primitiva. È qui che snapbend decide, per esempio, che una
svasatura va sul layer della svasatura e non su quello del foro.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class RenderContour:
    role:     str
    segments: List[Any]      = field(default_factory=list)
    styles:   List[Any]      = field(default_factory=list)
    polygon:  Optional[Any]  = None
