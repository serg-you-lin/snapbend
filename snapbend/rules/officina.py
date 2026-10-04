"""
snapbend/rules/officina.py
--------------------------
La cartella officina: i dati di chi usa snapbend (calibrazioni, spessori a
magazzino), fuori dal repo (MAP.md D60). Si sceglie in uno di due modi, il
primo vince: `set_officina(path)` in uno script, o la variabile d'ambiente
`SNAPBEND_OFFICINA`. Senza nessuno dei due si usano gli esempi generici del
repo.

    <officina>/calibrations/<nome>.json
    <officina>/sheet_thicknesses.json
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

OFFICINA_ENV = "SNAPBEND_OFFICINA"

_chosen: Optional[Path] = None


def set_officina(path) -> None:
    """Sceglie la cartella officina per questo programma (vince sulla variabile); None torna alla variabile."""
    global _chosen
    _chosen = None if path is None else Path(path)


def officina_folder() -> Optional[Path]:
    """La cartella officina scelta con `set_officina`, o quella di `SNAPBEND_OFFICINA`; None se nessuna."""
    value = str(_chosen) if _chosen is not None else os.environ.get(OFFICINA_ENV, "").strip()
    if not value:
        return None
    folder = Path(value)
    if not folder.is_dir():
        raise FileNotFoundError(f"cartella officina {value}: non esiste")
    return folder


def officina_file(*parts: str) -> Optional[Path]:
    """Un file dentro la cartella officina, se c'è una cartella officina e il file esiste."""
    folder = officina_folder()
    if folder is None:
        return None
    path = folder.joinpath(*parts)
    return path if path.is_file() else None
