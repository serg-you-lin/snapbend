"""
snapbend/flat/roles.py
----------------------
Vocabolario di processo — foro, foro filettato, svasatura, piega, incisione,
marcatura (arrivato da topo `tools/manufacturing_role.py`, topo MAP.md D88).

topo non conosce questi ruoli: `heal(doc, is_structural=...)` riceve
`is_structural` da qui (lo passa `heal_and_detect()`), e colori e layer di
output sono due mappe di snapbend, `ROLE_STYLES` e `LAYERS`, che chi
esporta passa a topo (`topo.to_dxf(result, role_styles=ROLE_STYLES,
layers=LAYERS)`) — topo non ne tiene nessuna (topo MAP.md D128).
"""

from __future__ import annotations

from typing import Dict

import topo

# ---------------------------------------------------------------------------
# I ruoli manifatturieri — stringhe semplici, non un ContourRole: il motore
# non deve poterli importare per nome. Confrontabili con `==` come qualunque
# altro ruolo (tutto in topo lo confronta per valore, mai per identità/tipo
# — vedi model/role.py::role_str).
# ---------------------------------------------------------------------------
HOLE          = "hole"
COUNTERSINK   = "countersink"
THREADED_HOLE = "threaded_hole"
BEND          = "bending"
ENGRAVE       = "engrave"
MARKING       = "marking"

# Quali di questi sono topologia di contorno di pezzo (un foro è un vero
# contorno interno, una piega/incisione/marcatura non lo è) — la stessa
# domanda che `model.role.STRUCTURAL_ROLES` risponde per outer/inner, qui
# estesa al vocabolario che il motore non conosce.
STRUCTURAL_MANUFACTURING_ROLES = frozenset({HOLE, COUNTERSINK, THREADED_HOLE})

# I ruoli che detect_flat() sa collocare come feature di un cluster (usato da
# detect.py per distinguere "proxy già classificato da role_rules" da "proxy
# ancora da inferire").
ALL_MANUFACTURING_ROLES = frozenset({HOLE, COUNTERSINK, THREADED_HOLE, BEND, ENGRAVE, MARKING})

# work_type stringa (RoleRule.role) → ruolo. Estende
# model.role.WORK_TYPE_TO_ROLE (che qui non tocchiamo) con i nomi
# manifatturieri — usata da detect/adapter quando serve il nome canonico.
WORK_TYPE_TO_ROLE: Dict[str, str] = {
    "hole":          HOLE,
    "bending":       BEND,
    "bend":          BEND,
    "countersink":   COUNTERSINK,
    "threaded_hole": THREADED_HOLE,
    "engrave":       ENGRAVE,
    "marking":       MARKING,
}


# Nomi layer DXF dell'output di snapbend — in `LAYERS` qui sotto, e la fonte
# di verità per chi (tipicamente i test) deve confrontare un layer scritto in
# output senza reinventare la stringa.
LAYER_HOLE          = "Hole"
LAYER_COUNTERSINK   = "Countersink"
LAYER_THREADED_HOLE = "ThreadHole"
LAYER_BENDING       = "Bending"
LAYER_ENGRAVE       = "Engrave"
LAYER_MARKING       = "Marking"


def is_structural(role) -> bool:
    """
    Predicato strutturale COMPLETO: outer/inner (motore) + hole/countersink/
    threaded_hole (manifatturiero). Questo è quello che `heal_and_detect()`
    passa a `heal(doc, is_structural=...)` — il motore da solo conosce solo
    la metà `model.role.is_structural_role`.
    """
    return topo.model.is_structural_role(role) or role in STRUCTURAL_MANUFACTURING_ROLES


# Colore di ogni ruolo di processo in uscita (gli RGB canonici dei vecchi ACI
# 6, 5, 4, 11, 9, 8 — l'11 è rosa, non bianco).
ROLE_STYLES: Dict[str, "topo.RoleStyle"] = {
    HOLE:          topo.RoleStyle(color=(255, 0, 255)),     # magenta
    COUNTERSINK:   topo.RoleStyle(color=(0, 0, 255)),       # blu
    THREADED_HOLE: topo.RoleStyle(color=(0, 255, 255)),     # ciano
    BEND:          topo.RoleStyle(color=(255, 127, 127)),   # rosa
    ENGRAVE:       topo.RoleStyle(color=(192, 192, 192)),   # grigio chiaro
    MARKING:       topo.RoleStyle(color=(128, 128, 128)),   # grigio scuro
}

# Layer DXF di ogni ruolo di processo in uscita.
LAYERS: Dict[str, str] = {
    HOLE:          LAYER_HOLE,
    COUNTERSINK:   LAYER_COUNTERSINK,
    THREADED_HOLE: LAYER_THREADED_HOLE,
    BEND:          LAYER_BENDING,
    ENGRAVE:       LAYER_ENGRAVE,
    MARKING:       LAYER_MARKING,
}
