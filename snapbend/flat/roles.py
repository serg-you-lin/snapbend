"""
snapbend/flat/roles.py
----------------------
Vocabolario di processo — foro, foro filettato, svasatura, piega, incisione,
marcatura (arrivato da topo `tools/manufacturing_role.py`, topo MAP.md D88).

topo non conosce questi ruoli: `heal(doc, is_structural=...)` riceve
`is_structural` da qui (lo passa `heal_and_detect()`), e i colori/layer di
output si registrano in topo con `register_role_style`, lo stesso meccanismo
di qualunque consumatore.
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


# Nomi layer DXF di default per l'output — registrati sotto via
# register_role_style, e la fonte di verità per chi (tipicamente i test)
# deve confrontare un layer scritto in output senza reinventare la stringa.
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


def _register_default_styles() -> None:
    """
    Registra colore + nome layer di default per i ruoli manifatturieri —
    stessi valori che stavano hardcoded in rules/palette.py e
    adapters/dxf/layers.py prima del refactor. Gira all'import di questo
    modulo (quindi automaticamente quando topo viene importato, dato che
    topo/__init__.py importa detect): zero regressione sull'output di
    default, zero sapere manifatturiero fuori da qui — detect si registra
    con lo stesso meccanismo pubblico (`register_role_style`) che userebbe
    un consumatore esterno, nessun trattamento privilegiato.
    """

    # Valori copiati da rules.palette.ACI_TO_HEX (mai dal commento accanto a
    # COLOR_BENDING — diceva "bianco" ma ACI 11 è "#ff7f7f", rosa: il
    # commento era sbagliato, il valore vero è quello della tabella hex).
    topo.register_role_style(HOLE,          topo.RoleStyle(color=(255, 0, 255),   layer_name=LAYER_HOLE))          # magenta, ACI 6
    topo.register_role_style(COUNTERSINK,   topo.RoleStyle(color=(0, 0, 255),     layer_name=LAYER_COUNTERSINK))   # blu, ACI 5
    topo.register_role_style(THREADED_HOLE, topo.RoleStyle(color=(0, 255, 255),   layer_name=LAYER_THREADED_HOLE)) # ciano, ACI 4
    topo.register_role_style(BEND,          topo.RoleStyle(color=(255, 127, 127), layer_name=LAYER_BENDING))       # rosa, ACI 11
    topo.register_role_style(ENGRAVE,       topo.RoleStyle(color=(192, 192, 192), layer_name=LAYER_ENGRAVE))       # grigio chiaro, ACI 9
    topo.register_role_style(MARKING,       topo.RoleStyle(color=(128, 128, 128), layer_name=LAYER_MARKING))       # grigio scuro, ACI 8


_register_default_styles()
