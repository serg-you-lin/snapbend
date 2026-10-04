"""
snapbend/flat/model/__init__.py
-------------------------------
Tipi prodotti da `detect_flat()`: la lettura di processo di un pezzo piano.
Si attaccano a `cluster.detected` di forge (l'overlay aperto, forge D44).
"""
from .hole import (
    Hole,
    HOLE_TYPE_UNKNOWN,
    HOLE_TYPE_PLAIN,
    HOLE_TYPE_COUNTERSINK,
    HOLE_TYPE_THREADED,
    VALID_HOLE_TYPES,
)
from .bending_line import BendingLine
from .engraving import Engraving
from .classified import ClassifiedEntity
from .render import RenderContour

__all__ = [
    "Hole",
    "HOLE_TYPE_UNKNOWN",
    "HOLE_TYPE_PLAIN",
    "HOLE_TYPE_COUNTERSINK",
    "HOLE_TYPE_THREADED",
    "VALID_HOLE_TYPES",
    "BendingLine",
    "Engraving",
    "ClassifiedEntity",
    "RenderContour",
]
