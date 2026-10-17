"""
snapbend/flat/__init__.py
-------------------------
Lettura di processo di un pezzo piano (file di taglio / sviluppo) sopra
topo: fori, svasature, filettati, pieghe, incisioni; il tratteggio delle pieghe. Richiede topo
installato (il resto di snapbend no). Arrivato da topo, topo MAP.md D88.

    from snapbend.flat import heal_and_detect
    result = heal_and_detect(topo.load_dxf("pezzo.dxf"))
"""

from .roles import (
    HOLE, COUNTERSINK, THREADED_HOLE, BEND, ENGRAVE, MARKING,
    LAYER_HOLE, LAYER_COUNTERSINK, LAYER_THREADED_HOLE, LAYER_BENDING,
    LAYER_ENGRAVE, LAYER_MARKING, is_structural,
)
from .thresholds import HOLE_DIAMETER_THRESHOLD
from .detect import detect_flat, describe_features, ALL_FEATURES
from .pipeline import heal_and_detect
from .trim import DashPattern, DashRule, trim_bending_lines
from .model import (
    Hole, BendingLine, Engraving, ClassifiedEntity,
    HOLE_TYPE_PLAIN, HOLE_TYPE_COUNTERSINK, HOLE_TYPE_THREADED,
)

__all__ = [
    "HOLE", "COUNTERSINK", "THREADED_HOLE", "BEND", "ENGRAVE", "MARKING",
    "LAYER_HOLE", "LAYER_COUNTERSINK", "LAYER_THREADED_HOLE", "LAYER_BENDING",
    "LAYER_ENGRAVE", "LAYER_MARKING", "is_structural",
    "HOLE_DIAMETER_THRESHOLD",
    "detect_flat", "describe_features", "ALL_FEATURES", "heal_and_detect",
    "DashPattern", "DashRule", "trim_bending_lines",
    "Hole", "BendingLine", "Engraving", "ClassifiedEntity",
    "HOLE_TYPE_PLAIN", "HOLE_TYPE_COUNTERSINK", "HOLE_TYPE_THREADED",
]
