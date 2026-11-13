"""
snapbend/flat/__init__.py
-------------------------
Lettura di processo di un pezzo piano (file di taglio / sviluppo) sopra
topo: fori, svasature, filettati, pieghe, incisioni; il tratteggio delle pieghe. Richiede topo
installato (il resto di snapbend no). Arrivato da topo, topo MAP.md D88.

    from snapbend.flat import detect_flat
    result = detect_flat(topo_dxf.load_dxf("pezzo.dxf"), features="all")
"""

from .roles import (
    HOLE, COUNTERSINK, THREADED_HOLE, BEND, ENGRAVE, MARKING, INVALID,
    LAYER_HOLE, LAYER_COUNTERSINK, LAYER_THREADED_HOLE, LAYER_BENDING,
    LAYER_ENGRAVE, LAYER_MARKING, LAYER_INVALID, ROLE_STYLES, LAYERS, is_structural,
)
from .thresholds import HOLE_DIAMETER_THRESHOLD
from .detect import detect_flat, describe_features, ALL_FEATURES
from .trim import DashPattern, DashRule, trim_bending_lines
from .model import (
    Hole, BendingLine, Engraving, ClassifiedEntity,
    HOLE_TYPE_PLAIN, HOLE_TYPE_COUNTERSINK, HOLE_TYPE_THREADED,
)

__all__ = [
    "HOLE", "COUNTERSINK", "THREADED_HOLE", "BEND", "ENGRAVE", "MARKING", "INVALID",
    "LAYER_HOLE", "LAYER_COUNTERSINK", "LAYER_THREADED_HOLE", "LAYER_BENDING",
    "LAYER_ENGRAVE", "LAYER_MARKING", "LAYER_INVALID", "ROLE_STYLES", "LAYERS", "is_structural",
    "HOLE_DIAMETER_THRESHOLD",
    "detect_flat", "describe_features", "ALL_FEATURES",
    "DashPattern", "DashRule", "trim_bending_lines",
    "Hole", "BendingLine", "Engraving", "ClassifiedEntity",
    "HOLE_TYPE_PLAIN", "HOLE_TYPE_COUNTERSINK", "HOLE_TYPE_THREADED",
]
