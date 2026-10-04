"""
snapbend/rules/officina.py
--------------------------
La cartella officina: i dati di chi usa snapbend (calibrazioni, spessori a
magazzino), fuori dal pacchetto (MAP.md D60, D62). Facoltativa: si sceglie
con `set_officina(path)` in uno script; senza, valgono i dati inclusi nel
pacchetto.

    <officina>/calibrations/<nome>.json
    <officina>/sheet_thicknesses.json
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

_chosen: Optional[Path] = None


def set_officina(path) -> None:
    """Sceglie la cartella officina per questo programma; None la toglie."""
    global _chosen
    _chosen = None if path is None else Path(path)


def officina_folder() -> Optional[Path]:
    """La cartella officina scelta con `set_officina`; None se nessuna."""
    if _chosen is None:
        return None
    if not _chosen.is_dir():
        raise FileNotFoundError(f"cartella officina {_chosen}: non esiste")
    return _chosen


def officina_file(*parts: str) -> Optional[Path]:
    """Un file dentro la cartella officina, se c'è una cartella officina e il file esiste."""
    folder = officina_folder()
    if folder is None:
        return None
    path = folder.joinpath(*parts)
    return path if path.is_file() else None
