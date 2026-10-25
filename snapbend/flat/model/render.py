"""
snapbend/flat/model/render.py
-----------------------------
Come un elemento di processo si fa disegnare dai renderer di topo.

topo disegna un elemento di `cluster.detected` dal suo `role` e dalla sua
geometria (topo D90): se ha `contours`, ognuno con `role`, `segments`,
`styles`. Segmenti che chiudono un giro, o elemento che è un vuoto
(`is_void`) → contorno chiuso; altrimenti una entità per primitiva
(`topo.model.feature_closed`, topo D168). È qui che snapbend decide, per esempio, che una
svasatura va sul layer della svasatura e non su quello del foro.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class RenderContour:
    role:     str
    segments: List[Any]      = field(default_factory=list)
    styles:   List[Any]      = field(default_factory=list)
