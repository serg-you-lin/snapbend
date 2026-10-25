"""
snapbend/flat/model/classified.py
---------------------------------
Una entità classificata da `detect_flat()` senza una classe dedicata
(marking, work_type custom). Finisce in `cluster.custom` del cluster che la
contiene; se nessuno la contiene la curva resta in `result.loose`.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import Any, Optional, Tuple


@dataclass
class ClassifiedEntity:
    """
    Risultato della classificazione di una entità da detect_flat().

    Prodotto da detect_flat(), consumato da inject() e write().

    Campi:
        work_type  : tipo lavorazione — chiave di WORK_TYPE_TO_LAYER
        confidence : 1.0 da special_layers, < 1.0 da geometria o agente
        source     : "special_layers" | "geometric" | "agent"
        data       : dati estratti pronti per CAM — inject() li usa direttamente
    """       
    work_type:  str
    confidence: float
    source:     str
    data:       dict = field(default_factory=dict)
    representative_point: Optional[Tuple[float, float]] = None
    # la curva di topo da cui viene (ClosedCurve o OpenCurve): l'appartenenza
    # a un cluster si legge sulla sua geometria intera (v. MAP.md D54)
    curve:      Any  = None