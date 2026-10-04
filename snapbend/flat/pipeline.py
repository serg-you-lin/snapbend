"""
snapbend/flat/pipeline.py
-------------------------
`heal_and_detect()`: `forge.heal()` + `detect_flat()` in un colpo solo, con il
predicato strutturale di processo (un foro è un contorno di pezzo). Arrivato
da forge `recipes.py` (forge MAP.md D88).
"""

from __future__ import annotations

import forge
from forge.model import ForgeDocument, ForgeResult

from .detect import detect_flat
from .roles import is_structural
from .thresholds import HOLE_DIAMETER_THRESHOLD


def heal_and_detect(doc: ForgeDocument, tolerance=None, label="", source_file="",
                    features="all",
                    max_drill_diameter: float = HOLE_DIAMETER_THRESHOLD,
                    bending_tolerance: float = 1.0,
                    engrave_tolerance: float = 1.0) -> ForgeResult:
    """
    heal() + detect_flat(). `detect_flat()` viene saltato se heal() non produce
    cluster validi (il result torna comunque, con `is_valid=False`).
    """
    result = forge.heal(doc, tolerance=tolerance, label=label, source_file=source_file,
                        is_structural=is_structural)
    if result.is_valid and result.clusters:
        detect_flat(result,
                    features=features,
                    max_drill_diameter=max_drill_diameter,
                    bending_tolerance=bending_tolerance,
                    engrave_tolerance=engrave_tolerance)
    return result
